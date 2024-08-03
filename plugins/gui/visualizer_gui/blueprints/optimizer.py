from flask import Blueprint, request, jsonify, abort
from sqlalchemy.ext.automap import automap_base
import hashlib
import logging
import base64
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def new_bp_optimizer(db, Base):
    # Create a new Blueprint
    bp_optimizer = Blueprint("bp_optimizer", __name__)

    # Function to calculate hash
    def calculate_hash(data):
        return hashlib.sha256(data).hexdigest()

    # Ensure application context is available
    Optimizations = Base.classes.optimizations
    Optimae = Base.classes.optimae

    # Endpoint for evaluator to fetch the latest optimum
    @bp_optimizer.route("/fetch_optimum", methods=["POST"])
    def fetch_optimum():
        try:
            content = request.json
            required_fields = ['optimization_id', 'current_optimum_hash']

            # Validate input data
            for field in required_fields:
                if field not in content:
                    return jsonify({"error": f"Missing field: {field}"}), 400

            optimization_id = content['optimization_id']
            current_optimum_hash = content['current_optimum_hash']

            latest_optimum = db.session.query(Optimae).filter_by(optimizer_id=optimization_id).order_by(Optimae.id.desc()).first()

            if not latest_optimum:
                return jsonify({"message": "No optimizations available for the given ID"}), 204

            if latest_optimum.optimum_hash == current_optimum_hash:
                return jsonify({"message": "No new optimum reported"}), 200

            return jsonify({
                "optimum": latest_optimum.optimum,
                "optimum_hash": latest_optimum.optimum_hash
            }), 200
        except Exception as e:
            logger.error(f"Error fetching optimum: {e}")
            abort(500)

    # Endpoint for optimizer to report a new optimum
    @bp_optimizer.route("/optimum_found", methods=["POST"])
    def optimum_found():
        try:
            content = request.json
            required_fields = ['optimizer_id', 'optimum', 'optimum_hash']

            # Validate input data
            for field in required_fields:
                if field not in content:
                    return jsonify({"error": f"Missing field: {field}"}), 400

            optimizer_id = content['optimizer_id']
            optimum_base64 = content['optimum']
            optimum_hash = content['optimum_hash']

            # Decode the Base64 encoded optimum
            optimum_pickled = base64.b64decode(optimum_base64)

            # Validate hash, just show a warning if invalid
            if calculate_hash(optimum_pickled) != optimum_hash:
                logger.warning("Optimum hash mismatch")
                #return jsonify({"error": "Optimum hash mismatch"}), 400

            new_optimum = Optimae(
                optimizer_id=optimizer_id,
                optimum=optimum_base64,  # Store the Base64 encoded data
                optimum_hash=optimum_hash
            )
            db.session.add(new_optimum)

            # Update the latest optimum hash in the optimizations table
            latest_optimization = db.session.query(Optimizations).filter_by(id=optimizer_id).first()
            if latest_optimization:
                latest_optimization.last_optimum_hash = optimum_hash

            db.session.commit()
            return jsonify({"message": "Optimum reported successfully"}), 201
        except Exception as e:
            logger.error(f"Error reporting optimum: {e}")
            abort(500)

    return bp_optimizer
