import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def calculate_sheets(material_w, material_h, parts):
    total_sheets = 0
    layouts = []
    
    for part in parts:
        part_w, part_h, qty = part
        fit_across = material_w // part_w
        fit_down = material_h // part_h
        per_sheet = fit_across * fit_down if fit_across > 0 and fit_down > 0 else 0
        sheets_needed = math.ceil(qty / per_sheet) if per_sheet > 0 else float('inf')
        total_sheets += sheets_needed
        layouts.append((part_w, part_h, fit_across, fit_down, sheets_needed))
    
    return total_sheets, layouts

def plot_cut_layout(material_w, material_h, layouts):
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, material_w)
    ax.set_ylim(0, material_h)
    ax.set_xticks(range(0, material_w + 1, 6))
    ax.set_yticks(range(0, material_h + 1, 6))
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    y_offset = 0
    colors = ["lightblue", "lightgreen", "lightcoral", "lightgray"]
    
    for i, (part_w, part_h, fit_across, fit_down, _) in enumerate(layouts):
        color = colors[i % len(colors)]
        for row in range(fit_down):
            for col in range(fit_across):
                x = col * part_w
                y = y_offset + row * part_h
                rect = patches.Rectangle((x, y), part_w, part_h, linewidth=1, edgecolor='black', facecolor=color, alpha=0.6)
                ax.add_patch(rect)
    
    ax.set_title("Cut Layout for 48\" x 96\" Sheet")
    plt.xlabel("Width (inches)")
    plt.ylabel("Height (inches)")
    st.pyplot(fig)

def main():
    st.title("Material Utilization Calculator")
    st.write("Enter the dimensions of your raw material and the pieces to be cut.")
    
    material_w = st.number_input("Raw Material Width (inches)", min_value=1, value=48)
    material_h = st.number_input("Raw Material Height (inches)", min_value=1, value=96)
    
    part_entries = st.text_area("Enter parts in the format: Width, Height, Quantity (one per line)", "46,36,204\n46,36,504\n45,30,1104")
    
    if st.button("Calculate"):        
        parts = [tuple(map(int, line.split(','))) for line in part_entries.strip().split('\n')]
        total_sheets, layouts = calculate_sheets(material_w, material_h, parts)
        
        st.write(f"Total Sheets Required: **{total_sheets}**")
        plot_cut_layout(material_w, material_h, layouts)

if __name__ == "__main__":
    main()
