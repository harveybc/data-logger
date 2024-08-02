from flask import Blueprint, request, jsonify, abort
from sqlalchemy.ext.automap import automap_base
import hashlib
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def new_bp(plugin_folder, core_ep, store_ep, db, Base):
    # Create a new Blueprint
    bp_optimizer = Blueprint("bp_optimizer", __name__)

    # Function to calculate hash
    def calculate_hash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    # Ensure application context is available
    Optimizations = Base.classes.optimizations
    Optimae = Base.classes.optimae

    # Endpoint for evaluator to fetch the latest optimum
    @bp_optimizer.route("/fetch_optimum", methods=["POST"])
    def fetch_optimum():
        try:
            content = request.json
            required_fields = ['current_optimum_hash']

            # Validate input data
            for field in required_fields:
                if field not in content:
                    return jsonify({"error": f"Missing field: {field}"}), 400

            current_optimum_hash = content['current_optimum_hash']

            latest_optimization = db.session.query(Optimizations).filter_by(status='active').order_by(Optimizations.id.desc()).first()
            
            if not latest_optimization:
                return jsonify({"message": "No optimizations available"}), 204

            if latest_optimization.last_optimum_hash == current_optimum_hash:
                return jsonify({"message": "No new optimum reported"}), 200

            latest_optimum = db.session.query(Optimae).filter_by(optimum_hash=latest_optimization.last_optimum_hash).first()

            if not latest_optimum:
                return jsonify({"error": "Optimum not found"}), 404

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
            optimum = content['optimum']
            optimum_hash = content['optimum_hash']

            # Validate hash
            if calculate_hash(optimum) != optimum_hash:
                return jsonify({"error": "Optimum hash mismatch"}), 400

            new_optimum = Optimae(
                optimizer_id=optimizer_id,
                optimum=optimum,
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
