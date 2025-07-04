from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

from config import REF_PRICE, LOWER_THRESHOLD, UPPER_THRESHOLD, SCORE_AT_LOWER, SCORE_AT_UPPER, SIGMOID_K, SIGMOID_X0
from bids import bids
from curves import sigmoid

def evaluate_sigmoid():
    # Calcular preços limite
    # min_price = LOWER_THRESHOLD * REF_PRICE
    max_price = UPPER_THRESHOLD * REF_PRICE

    # Generar marca temporal
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    # Definir carpeta de salida
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Calcular puntos y status de las ofertas
    results = []
    for b in bids:
        score = sigmoid(b.price)
        status = "OK" if(b.price <= max_price) else "FORA"
        if status == "FORA":
            score = 0
        results.append((b.id, b.price, score, status))
    
    # Print to console
    print("\n")
    header = f"{'ID':<12}{'Preço (€)':<24}{'Pontuação':<14}{'Status':<12}"
    sep = "-" * len(header)
    print(header)
    print(sep)
    for bid_id, price, score, status in results:
        pontos_str = f"{score:<14.6f}" if status == "OK" else " " * 14
        print(f"{bid_id:<12}{price:<24,.2f}{pontos_str}{status:<12}")
    
    # Formula and constants used
    formula_str = "CurvaSigmoide: Pont = 1 / (1 + e^(k * (x_rel - x0)))"
    #    score = 1 / (1 + e^(k * (x_rel - x0)))
    #    score = 1 / (1 + eᵏ⁽ˣʳᵉˡ ⁻ ˣ⁰⁾)
    #    score = \frac{1}{1 + e^{k(x_{rel} - x_0)}}
    constants_str = f"k = {SIGMOID_K:.4f}, x0 = {SIGMOID_X0:.4f} (x_rel = price/REF_PRICE - 1)"

    # Print to .txt file with timestamp
    txt_filename = os.path.join(output_folder, f"{timestamp}_sigmoidEvaluationPreco.txt")
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(formula_str + "\n")
        f.write(constants_str + "\n\n")
        f.write(header + "\n")
        f.write(sep + "\n")
        for bid_id, price, score, status in results:
            pontos_str = f"{score:<14.6f}" if status == "OK" else " " * 14
            f.write(f"{bid_id:<12}{price:<24,.2f}{pontos_str}{status:<12}\n")
    print(f"\nTable saved to: {txt_filename}")

    # Construir curva sigmoide
    xs = np.linspace(0,
                     UPPER_THRESHOLD * REF_PRICE, 1000)
    ys = [sigmoid(x) for x in xs]

    plt.figure(figsize=(16, 7))
    
    # Plot curve. Marca los límites de la curva (en leyenda) para referencia interna
    plt.plot(xs, ys, label=f"CurvaEvalSigmoide ({LOWER_THRESHOLD:.2f}_{SCORE_AT_LOWER:.4f} <----> {UPPER_THRESHOLD:.2f}_{SCORE_AT_UPPER:.4f})", color='blue', linewidth=1)
    # plt.plot(xs, ys, label="CurvaEvalSigmoidePreço", color='blue', linewidth=1.5)
    
    # Líneas verticales (BASE e ANORM. BAIXO)
    upper_x = UPPER_THRESHOLD * REF_PRICE
    avg_bid = np.mean([price for _, price, _, status in results if status != "FORA"])
    anorm_x = avg_bid * 0.8  # 20% below average of all bids

    plt.axvline(upper_x, color='red', linestyle='--', linewidth=1)
    plt.axvline(anorm_x, color='brown', linestyle='--', linewidth=0.5)
    
    # Personalizar ticks en el eje x
    ticks = list(plt.xticks()[0])
    if upper_x not in ticks:
        ticks.append(upper_x)
    if anorm_x not in ticks:
        ticks.append(anorm_x)
    ticks = sorted(ticks)

    def format_milions(x, pos=None):
        if abs(x - upper_x) < 1e-6:
            val = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"{val} M€\nPREÇO BASE"
        elif abs(x - anorm_x) < 1e-6:
            val = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"\n\n{val} M€\nPREÇO ANORM. BAIXO"
        else:
            return f"{x/1e6:.1f}M€"
    
    plt.xticks(ticks, [format_milions(t) for t in ticks], fontsize = 8, rotation = 0)

    ax = plt.gca()
    labels = ax.get_xticklabels()
    for i, t in enumerate(ticks):
        if abs(t - upper_x) < 1e-6:
            labels[i].set_color('red')
            labels[i].set_ha('left')
        elif abs(t - anorm_x) < 1e-6:
            labels[i].set_color('brown')
            # labels[i].set_rotation(45)
            labels[i].set_ha('center')
    ax.set_xticklabels(labels)

    # Mark bids
    for bid_id, price, score, status in results:
        if status == "OK":
            plt.scatter(price, score, s=25, marker= "o", label=f"{bid_id} - {price:,.2f}€ - {score:.4f} pontos")
        else:
            plt.scatter(price, score, s=15, marker="x", color='red', label=f"{bid_id} - {price:,.2f}€ - {score:.4f} pontos (FORA)")
    
    plt.xlabel("PREÇO (€)")
    plt.ylabel("PONTUAÇÃO (0–100)")
    plt.title("CURVA SIGMOIDE DE AVALIAÇÃO DE PREÇO", pad=40)
    plt.xlim(0, UPPER_THRESHOLD * REF_PRICE * 1.1)  # X axis from 0 to max + 10% margin to the left
    # plt.xticks(ticks, rotation=45)  # Rotate x-ticks for better visibility
    plt.ylim(-5, 105) # Y axis from 0 to 100 + 5% margin
    plt.yticks(np.arange(0, 101, 10))  # Tick every 10 points
    plt.grid(True)

    # Visulaización de ejes
    for spine in plt.gca().spines.values():
        # spine.set_color('#cccccc')
        spine.set_linewidth(0.5)

    plt.tight_layout()
    
    plt.legend(
        loc='lower left',
        bbox_to_anchor=(0, -0.60, 1, 1),
        # mode="expand",
        ncol=1,
        borderaxespad=0,
        frameon=False,
    )

    # Formula y constantes en gráfico
    plt.figtext(0.53, 0.9, formula_str + "\n" + constants_str, wrap=True, ha='center', fontsize=9)

    # Save to PNG with timestamp
    png_filename = os.path.join(output_folder, f"{timestamp}_sigmoidEvaluation.png")
    plt.savefig(png_filename, bbox_inches='tight')
    plt.close()
    print(f"\nPlot saved as: {png_filename}")
    print("\n")

if __name__ == "__main__":
    evaluate_sigmoid()