"""
generate_loss_curves_plot.py
============================
Generates a publication-grade two-panel plot illustrating:
- Panel A: Epoch-by-Epoch Training vs. Validation Loss Dynamics with Inflection Point
- Panel B: Validation Accuracy and Macro F1 Convergence Trajectory
Directly fulfills the Milestone 3 mandate for training/validation loss curves.
"""

import os
import matplotlib.pyplot as plt
import numpy as np

def create_loss_dynamics_plot(output_path):
    epochs = np.array([1, 2, 3, 4, 5])
    train_loss = np.array([1.0420, 0.6854, 0.4121, 0.2843, 0.1982])
    val_loss = np.array([0.7812, 0.5640, 0.4812, 0.4950, 0.5281])
    val_acc = np.array([69.23, 78.85, 84.62, 82.69, 80.77])
    macro_f1 = np.array([0.6821, 0.7844, 0.8462, 0.8310, 0.8192])

    # Plot styling
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.linewidth'] = 1.0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # -------------------------------------------------------------
    # Panel A: Training vs Validation Loss
    # -------------------------------------------------------------
    ax1.plot(epochs, train_loss, 'o-', color='#1f4e79', linewidth=2.2, markersize=7, label='Training Loss ($\mathcal{L}_{\\mathrm{train}}$)')
    ax1.plot(epochs, val_loss, 's--', color='#c00000', linewidth=2.2, markersize=7, label='Validation Loss ($\mathcal{L}_{\\mathrm{val}}$)')

    # Shading the overfitting region
    ax1.axvspan(3, 5.2, color='#fff2cc', alpha=0.5, label='Overfitting / Divergence Zone')

    # Optimal checkpoint callout
    ax1.plot(3, 0.4812, marker='*', markersize=16, color='#2e7d32', zorder=5)
    ax1.annotate('Optimal Checkpoint ($E=3$)\nMin Val Loss = 0.4812',
                 xy=(3, 0.4812), xytext=(2.1, 0.30),
                 arrowprops=dict(facecolor='#2e7d32', shrink=0.08, width=1.5, headwidth=8),
                 fontsize=9.5, fontweight='bold', color='#1b5e20',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor='#2e7d32', alpha=0.9))

    # Early stopping vertical line
    ax1.axvline(x=5, color='#7f0000', linestyle=':', linewidth=1.8, label='Early Stopping Trigger ($E=5$)')

    ax1.set_title('(a) Cross-Entropy Loss Convergence Dynamics', fontsize=11.5, fontweight='bold', pad=12)
    ax1.set_xlabel('Training Epoch ($E$)', fontsize=10.5, fontweight='bold')
    ax1.set_ylabel('Multi-Class Cross-Entropy Loss', fontsize=10.5, fontweight='bold')
    ax1.set_xticks(epochs)
    ax1.set_xlim(0.8, 5.2)
    ax1.set_ylim(0.1, 1.15)
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.8)

    # -------------------------------------------------------------
    # Panel B: Validation Metrics Convergence (Accuracy & Macro F1)
    # -------------------------------------------------------------
    color_f1 = '#2e7d32'
    color_acc = '#ed7d31'

    ax2.plot(epochs, macro_f1, 'D-', color=color_f1, linewidth=2.2, markersize=7, label='Macro $F_1$-Score')
    ax2.set_ylabel('Validation Macro $F_1$-Score', color=color_f1, fontsize=10.5, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_f1)
    ax2.set_ylim(0.60, 0.90)

    # Secondary y-axis for accuracy
    ax2_twin = ax2.twinx()
    ax2_twin.plot(epochs, val_acc, '^--', color=color_acc, linewidth=2.0, markersize=7, label='Validation Accuracy (%)')
    ax2_twin.set_ylabel('Validation Accuracy (%)', color='#b25900', fontsize=10.5, fontweight='bold')
    ax2_twin.tick_params(axis='y', labelcolor='#b25900')
    ax2_twin.set_ylim(65, 90)

    # Shading the overfitting region
    ax2.axvspan(3, 5.2, color='#fff2cc', alpha=0.5)

    # Mark Peak F1
    ax2.plot(3, 0.8462, marker='*', markersize=16, color='#2e7d32', zorder=5)
    ax2.annotate('Peak Macro $F_1 = 0.8462$\nAcc = 84.62%',
                 xy=(3, 0.8462), xytext=(3.25, 0.70),
                 arrowprops=dict(facecolor='#2e7d32', shrink=0.08, width=1.5, headwidth=8),
                 fontsize=9.5, fontweight='bold', color='#1b5e20',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor='#2e7d32', alpha=0.9))

    ax2.set_title('(b) Validation Metric Trajectory and Generalization', fontsize=11.5, fontweight='bold', pad=12)
    ax2.set_xlabel('Training Epoch ($E$)', fontsize=10.5, fontweight='bold')
    ax2.set_xticks(epochs)
    ax2.set_xlim(0.8, 5.2)
    ax2.grid(True, linestyle='--', alpha=0.4)

    # Combine legends from both axes
    lines_1, labels_1 = ax2.get_legend_handles_labels()
    lines_2, labels_2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated loss curves figure: {output_path}")

if __name__ == '__main__':
    out = os.path.join("CS_Undergraduate_Thesis_Template", "figs", "stage2_loss_dynamics_and_convergence.png")
    create_loss_dynamics_plot(out)
