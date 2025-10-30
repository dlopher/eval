import argparse
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import os

from src.config.config_price import MAX_SCORE, MIN_SCORE, MAX_PRICE, REF_PRICE, LOWER_THRESHOLD, UPPER_THRESHOLD, SCORE_AT_LOWER, SCORE_AT_UPPER, SIGMOID_K, SIGMOID_X0
from src.models.bids_price import bids, calc_abnormally_low_bid, generate_test_bids
from src.utils.curves import sigmoid, linear, semicircle, inverse_proportional, exponential

def evaluate_bids(curve_functions=None, curve_names=None, test_mode=False):
    """
    Evaluates bids using the specified curve function(s).
    
    Parameters:
        curve_functions: List of curve functions to use
        curve_names: Names of the curves for display purposes
        test_mode: If True, uses generated test bids instead of competition bids
    """
    # Generar marca temporal
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    # Definir carpeta de salida
    output_folder = "data/output"
    os.makedirs(output_folder, exist_ok=True)
    
    if curve_functions is None:
        curve_functions = [semicircle]
    if curve_names is None:
        curve_names = ["semicircle"]

    is_multi_curve = len(curve_functions) > 1
    
    # Calcular preço base
    max_price = MAX_PRICE

    evaluation_bids = generate_test_bids() if test_mode else bids

    # Pre-determine which bids are accepted and calculate anorm_x once
    bid_statuses = [(b.id, b.name, b.price, "OK" if b.price <= max_price else "FORA") for b in evaluation_bids]
    accepted_prices = [price for _, _, price, status in bid_statuses if status == "OK"]
    anorm_x = calc_abnormally_low_bid(accepted_prices)

    # Prearar los resultados de CADA curva
    all_results = []

    for i, curve_function in enumerate(curve_functions):
        # Calcular puntuación de las ofertas usando cada curva
        results = []
        for bid_id, name, price, status in bid_statuses:
            if status == "FORA":
                score = 0
            else:
                score = curve_function(price, min_score=MIN_SCORE, max_score=MAX_SCORE)
            # Mark abnormally low bids
            pab = "x" if (status == "OK" and price <= anorm_x) else ""
            results.append((bid_id, name, price, score, status, pab))

        all_results.append((results, curve_names[i], curve_function))

    # Print to console
    for results, curve_name, curve_function in all_results:
        print("\n")
        print(f"\n{curve_name.upper()} CURVE EVALUATION:")
        header = f"{'ID':<12}{'Nome':<24}{'Preço (€)':<24}{'Pontuação':<14}{'Status':<12}{'PAB':<6}"
        sep = "-" * len(header)
        print(header)
        print(sep)
        for bid_id, name, price, score, status, pab in results:
            pontos_str = f"{score:<14.6f}" if status == "OK" else " " * 14
            print(f"{bid_id:<12}{name:<24}{price:<24,.2f}{pontos_str}{status:<12}{pab:<6}")

    # Print to .txt file with timestamp
    if bids:
        curve_names_str = "_".join(curve_names)
        txt_filename = os.path.join(output_folder, f"{timestamp}_{curve_names_str}_EvaluacaoPreco.txt")
        
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("CURVE EVALUATION RESULTS\n")
            f.write("=" * 80 + "\n\n")

            for results, curve_name, curve_function in all_results:
                f.write(f"\n{curve_name.upper()} CURVE EVALUATION:\n")
                f.write("-" * 50 + "\n")

                # Write formula and constants
                if curve_function == sigmoid:
                    formula_str = "P = 1 / (1 + e^(k * (x_rel - x0)))"
                    #               score = 1 / (1 + eᵏ⁽ˣʳᵉˡ ⁻ ˣ⁰⁾)
                    constants_str = f"k = {SIGMOID_K:.4f} || x0 = {SIGMOID_X0:.4f} || x_rel = ((OFERTA/ref_price) - 1)"
                elif curve_function == linear:
                    formula_str = "P = 100 * (UPPER_THRESHOLD - (price/REF_PRICE)) / (UPPER_THRESHOLD - LOWER_THRESHOLD)"
                    constants_str = f"LOWER_THRESHOLD = {LOWER_THRESHOLD:.2f} || UPPER_THRESHOLD = {UPPER_THRESHOLD:.2f}"
                elif curve_function == semicircle:
                    formula_str = "P = 100 * sqrt(1 - x²)"
                    constants_str = f"x = price / (MAX_PRICE)"
                elif curve_function == exponential:
                    formula_str = "P = 100 * e^(-x)"
                    constants_str = f"x = price / (MAX_PRICE)"
                else:
                    formula_str = "Custom curve"
                    constants_str = ""
                
                f.write(f"Formula: {formula_str}\n")
                f.write(f"Constants: {constants_str}\n\n")

                # Write table header
                header = f"{'ID':<12}{'Nome':<24}{'Preço (€)':<24}{'Pontuação':<14}{'Status':<12}{'PAB':<6}"
                sep = "-" * len(header)
                f.write(header + "\n")
                f.write(sep + "\n")

                # Write bid results
                for bid_id, name, price, score, status, pab in results:
                    pontos_str = f"{score:<14.6f}" if status == "OK" else " " * 14
                    f.write(f"{bid_id:<12}{name:<24}{price:<24,.2f}{pontos_str}{status:<12}{pab:<6}\n")

            f.write("\n" + "=" * 80 + "\n")

        print(f"\nCombined table saved to: {txt_filename}")
    else:
        print("\nNo bids to evaluate. Skipping file creation.")

    # Create plot
    plt.figure(figsize=(16, 10))

    # x-axis data
    xs = np.linspace(0, MAX_PRICE, 1000)
    
    # Plot curves
    colors = ['blue', 'green', 'orange', 'purple', 'pink']
    
    for i, (results, curve_name, curve_function) in enumerate(all_results):
        ys = [curve_function(x, min_score=MIN_SCORE, max_score=MAX_SCORE) for x in xs]
        if curve_function == sigmoid:
            plt.plot(xs, ys, label=f"Curva {curve_name.capitalize()}"
                     f"({LOWER_THRESHOLD:.2f}_{SCORE_AT_LOWER:.4f} <----> {UPPER_THRESHOLD:.2f}_{SCORE_AT_UPPER:.4f})",
                 color=colors[i % len(colors)], linewidth=1.5)
        else:
            plt.plot(xs, ys, label=f"Curva {curve_name.capitalize()}",
                    color=colors[i % len(colors)], linewidth=1.5)

    # Líneas verticales (BASE e ANORM. BAIXO)
    upper_x = MAX_PRICE
    plt.axvline(upper_x, color='red', linestyle='--', linewidth=1)
    
    if anorm_x and anorm_x > 0:
        plt.axvline(anorm_x, color='brown', linestyle='--', linewidth=0.5)

    # Personalizar ticks en el eje x
    ticks = list(plt.xticks()[0])
    if upper_x not in ticks:
        ticks.append(upper_x)
    if anorm_x > 0:
        if anorm_x not in ticks:
            ticks.append(anorm_x)
    
    ticks = sorted(ticks)

    def format_milions(x, pos=None):
        if abs(x - upper_x) < 1e-6:
            val = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"{val} M€\nPREÇO BASE"
        elif anorm_x > 0 and abs(x - anorm_x) < 1e-6:
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
        elif anorm_x > 0 and abs(t - anorm_x) < 1e-6:
            labels[i].set_color('brown')
            # labels[i].set_rotation(45)
            labels[i].set_ha('center')
    ax.set_xticklabels(labels)

    # Assign colors to unique bids (by bid_id)
    bid_colors = {}
    bid_markers = {}
    unique_bids = set()

    for results, _, _ in all_results:
        for bid_id, _, _, _, status, pab in results:
            unique_bids.add(bid_id)

            # Assign markers
            if status == "FORA":
                bid_markers[bid_id] = ("x", 15, 'red')
            elif pab == "x":
                bid_markers[bid_id] = ("x", 15, None)
            else:
                bid_markers[bid_id] = ("o", 25, None)
    
    # Assign colors to each bid
    bid_palette = plt.colormaps['tab10']
    for i, bid_id in enumerate(sorted(unique_bids)):
        bid_colors[bid_id] = bid_palette(i)

    # Mark bids on the plot
    for curve_idx, (results, curve_name, _) in enumerate(all_results):
        for bid_id, name, price, score, status, pab in results:
            marker, size, color = bid_markers[bid_id]
            if color is None:
                color = bid_colors[bid_id]
            
            # Include curve name in the label.
            if status == "FORA":
                label = f"{name} ({bid_id}) - {price:,.2f}€ - FORA ({curve_name})"
            else:
                label = f"{name} ({bid_id}) - {price:,.2f}€ - {score:.2f} pts ({curve_name})"
                if pab == "x":
                    label += " - (PAB)"
            
            plt.scatter(price, score, s=size, marker=marker, color=color, label=label, alpha=0.8)

    
    # Format plot
    plt.xlabel("PREÇO (€)")
    plt.ylabel("PONTUAÇÃO (0–100)")

    if is_multi_curve:
        title = f"COMPARAÇÃO DE CURVAS DE AVALIAÇÃO DE PREÇO ({' - '.join(curve_names)})"
    else:
        title = f"CURVA DE AVALIAÇÃO DE PREÇO ({curve_names[0]})"
    
    plt.title(title, pad=40)
    
    plt.xlim(0, MAX_PRICE * 1.1)  # X axis from 0 to max + 10% margin to the left
    # plt.xticks(ticks, rotation=45)  # Rotate x-ticks for better visibility
    plt.ylim(-5, 105) # Y axis from 0 to 100 + 5% margin
    plt.yticks(np.arange(0, 101, 10))  # Tick every 10 points
    plt.grid(True)

    # Visualización de ejes
    for spine in plt.gca().spines.values():
        # spine.set_color('#cccccc')
        spine.set_linewidth(0.5)

    plt.tight_layout()
    
    # Add legends
    # Create two separate legends: one for curves, one for bids
    
    # 1. Create curve legend first (at the usual position)
    curve_handles = []
    curve_labels = []
    
    # Get line objects for curves
    for i, (results, curve_name, curve_function) in enumerate(all_results):
        line = plt.gca().get_lines()[i]  # Get the line for this curve
        curve_handles.append(line)
        
        # Create appropriate label based on curve type
        if curve_function == sigmoid:
            curve_labels.append(f"Curva {curve_name.capitalize()} ({LOWER_THRESHOLD:.2f}_{SCORE_AT_LOWER:.1f} <-> {UPPER_THRESHOLD:.2f}_{SCORE_AT_UPPER:.1f})")
        else:
            curve_labels.append(f"Curva {curve_name.capitalize()}")
    
    # Place curves legend at lower left (original position)
    first_legend = plt.legend(
        curve_handles, curve_labels,
        loc='lower left',
        bbox_to_anchor=(0, -0.5, 1, 1),
        ncol=1,  # Only one column
        frameon=False,
        fontsize='small'
    )
    
    # Add the first legend manually to keep it
    plt.gca().add_artist(first_legend)
    
    # 2. Create bids legend second (at the bottom)
    bid_handles = []
    bid_labels = []
    
    # Process and group bid markers
    handles, labels = [], []
    for curve_idx, (results, curve_name, _) in enumerate(all_results):
        for bid_id, name, price, score, status, pab in results:
            # Get scatter point object
            scatter_idx = curve_idx * len(results) + results.index((bid_id, name, price, score, status, pab))
            scatter = plt.gca().collections[scatter_idx]
            handles.append(scatter)
            
            # Format label
            if status == "FORA":
                label = f"{name} {bid_id} - {price:,.2f}€ - FORA ({curve_name})"
            else:
                label = f"{name} {bid_id} - {price:,.2f}€ - {score:.2f} pts ({curve_name})"
                if pab == "x":
                    label += " - (PAB)"
            labels.append(label)
    
    # Group by bid_id
    by_bid = {}
    for h, l in zip(handles, labels):
        bid_id = int(l.split()[1])  # Convert to integer for proper numeric sorting
        if bid_id not in by_bid:
            by_bid[bid_id] = []
        by_bid[bid_id].append((h, l))
    
    # Flatten the grouped bids
    for bid_id in sorted(by_bid.keys()):  # Now sorted numerically
        for h, l in by_bid[bid_id]:
            bid_handles.append(h)
            bid_labels.append(l)
    
    # Place bids legend
    second_legend = plt.legend(
        bid_handles, bid_labels,
        loc='upper left',
        bbox_to_anchor=(0, -0.6),
        ncol=4,
        borderaxespad=0,
        frameon=True,
        fontsize='small'
    )

    plt.subplots_adjust(bottom=0.3)  # Adjust bottom margin for legend

    # Formula y constantes en debajo del título
    # plt.figtext(0.53, 0.9, formula_str + "\n" + constants_str, wrap=True, ha='center', fontsize=9)

    # Save to PNG with timestamp
    curve_names_str = "_".join(curve_names)
    png_filename = os.path.join(output_folder, f"{timestamp}_{curve_names_str}Evaluation.png")
    plt.savefig(png_filename, bbox_inches='tight')
    plt.close()
    print(f"\nPlot saved as: {png_filename}")
    print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate bids using different curves.')
    parser.add_argument('--curves', '-c', type=str, nargs='+',
                        choices=['sigmoid', 'linear', 'semicircle', 'inverse', 'exponential'],
                        default=['sigmoid'],
                        help='Curve type(s) for evaluation (default: sigmoid). Multiple curves can be specified.')
    parser.add_argument('--test', '-t',action='store_true',
                        help='Run in test mode with auto-generated bids.')

    args = parser.parse_args()

    # Map curve names to functions
    curve_map = {
        'sigmoid': sigmoid,
        'linear': linear,
        'semicircle': semicircle,
        'inverse': inverse_proportional,
        'exponential': exponential
    }

    if len(args.curves) == 0:
        print("No curves specified. Using sigmoid as default.")
        args.curves = ['sigmoid']

    # Check for uniqueness in curve list
    unique_curves = []
    for curve in args.curves:
        if curve not in unique_curves:
            unique_curves.append(curve)
    
    curve_functions = [curve_map[c] for c in unique_curves]
    print(f"\nUsing {', '.join(unique_curves)} curve(s) for evaluation.")

    evaluate_bids(curve_functions, unique_curves, test_mode=args.test)