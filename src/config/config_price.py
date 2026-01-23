import math


###------ SCORING CONFIGURATION ------###
# Puntuaciones en los "valores de control" (puntos en escala 0-100)
SCORE_AT_LOWER = 80    
SCORE_AT_UPPER = 1
# ES RESTELO: 0.9 --> 90 // 1.2 --> 1
MAX_SCORE = 100.0  # Scale reference

# Derivar MIN_SCORE from MAX_SCORE (what sigmoid asymptotically approaches)
MIN_SCORE = SCORE_AT_UPPER

###------ SIGMOIDE PARAMETERS ------###
# Limites asumibles(SIEMPRE como fracciones de REF_PRICE)
LOWER_THRESHOLD = 0.80
UPPER_THRESHOLD = 1.15

MAX_PRICE = 953_405.00

# Precio de referencia (euros)
# ES RESTELO = 1_050_000.00
REF_PRICE = MAX_PRICE / UPPER_THRESHOLD

# Conversion en fracciones normalizadas (0-1) para el calculo en sigmoide
s_low = SCORE_AT_LOWER / MAX_SCORE
s_up  = SCORE_AT_UPPER  / MAX_SCORE

# Relative positions (x_rel = price/REF_PRICE – 1)
L_rel = LOWER_THRESHOLD - 1.0
U_rel = UPPER_THRESHOLD - 1.0

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

# print(f"SIGMOIDE k: {SIGMOID_K}")

# 2) then from α_low = exp[k*(L_rel – x0)]  ⇒  x0 = L_rel - ln(α_low)/k
SIGMOID_X0 = L_rel - (math.log(alpha_low) / SIGMOID_K)

# print(f"SIGMOIDE x0: {SIGMOID_X0}")