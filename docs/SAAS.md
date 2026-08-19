# Servicio multiusuario (después del alpha)

## Login y pagos

- **Humanos en la web:** Google Sign-In (OAuth 2). Cada cuenta se liga a
  un sitio. Beta: `plan=beta` (gratis). Luego `plan=pago`.
- **Cobro en la web (Colombia):** Mercado Pago o Stripe. “Google
  Payments” / Play Billing es para apps de la Play Store, no para un
  SaaS de navegador.
- **Dispositivos:** siguen con token de ThingsBoard. Eso no es el login
  del ganadero.

No se implementa OAuth ni cobros en el lote de casa. El software sigue
MIT; el contrato del servicio es otro documento.

## AAA

| Quién | Cómo |
|---|---|
| ESP32 / Hermes | Access token de ThingsBoard |
| Operador del sitio | Google (futuro) o, hoy, la red local |
| Nosotros | Tenant / sysadmin de ThingsBoard |

Un usuario de Google no debe ser `tenant@thingsboard.org`.
