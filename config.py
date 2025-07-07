import math

# Precio de referencia (euros)
REF_PRICE = 1_053_496.00

# Limites asumibles(SIEMPRE como fracciones de REF_PRICE)
LOWER_THRESHOLD = 0.80   # 20% ABAJO
UPPER_THRESHOLD = 1.20   # 20% ARRIBA

# Puntuaciones para los límites (escala 0–100)
SCORE_AT_LOWER = 90    
SCORE_AT_UPPER =  1

# Conversion en fracciones
s_low = SCORE_AT_LOWER / 100.0
s_up  = SCORE_AT_UPPER  / 100.0

# Relative positions (x_rel = price/REF_PRICE – 1)
L_rel = LOWER_THRESHOLD - 1.0   # e.g. 0.90 – 1 = –0.10
U_rel = UPPER_THRESHOLD - 1.0   # e.g. 1.20 – 1 = +0.20

# For a logistic of the form
#   score_frac(x_rel) = 1 / (1 + exp(  k*(x_rel – x0)  )),
# we need to solve for k and x0 given:
#   score_frac(L_rel) = s_low
#   score_frac(U_rel) = s_up

# 1) α_low  = exp( k*(L_rel – x0) ) = (1/s_low) – 1
# 2) α_up   = exp( k*(U_rel – x0) ) = (1/s_up)  – 1
# ⇒ dividing (1)/(2):
#    exp[ k*(L_rel – U_rel) ] = α_low / α_up
# ⇒  k = ln(α_low/α_up) / (L_rel – U_rel)

alpha_low = (1.0 / s_low) - 1.0
alpha_up  = (1.0 / s_up)  - 1.0

SIGMOID_K  = math.log(alpha_low / alpha_up) / (L_rel - U_rel)

print("\n")
print(f"SIGMOIDE k: {SIGMOID_K}")

# 2) then from α_low = exp[k*(L_rel – x0)]  ⇒  x0 = L_rel - ln(α_low)/k
SIGMOID_X0 = L_rel - (math.log(alpha_low) / SIGMOID_K)

print("\n")
print(f"SIGMOIDE x0: {SIGMOID_X0}")