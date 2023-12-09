def best_fit_decreasing_with_cut_details(original_materials, cut_specifications):
    sorted_cuts = sorted(cut_specifications, reverse=True, key=lambda x: x[0])

    materials = [
        {"length": length, "quantity": quantity, "remaining": length, "cuts": []}
        for length, quantity in original_materials
    ]

    used_materials = {
        length: {"used": 0, "cut_details": []} for length, _ in original_materials
    }

    for cut_length, cut_quantity in sorted_cuts:
        for _ in range(cut_quantity):
            best_fit = None
            min_waste = float("inf")

            for material in materials:
                if (
                    material["remaining"] >= cut_length
                    and material["remaining"] - cut_length < min_waste
                    and material["quantity"] > 0
                ):
                    best_fit = material
                    min_waste = material["remaining"] - cut_length

            if best_fit:
                best_fit["cuts"].append(cut_length)
                best_fit["remaining"] -= cut_length

                if best_fit["remaining"] < min(
                    [length for length, _ in cut_specifications]
                ):
                    best_fit["quantity"] -= 1
                    used_materials[best_fit["length"]]["used"] += 1
                    used_materials[best_fit["length"]]["cut_details"].append(
                        best_fit["cuts"].copy()
                    )
                    best_fit["cuts"].clear()
                    if best_fit["quantity"] > 0:
                        best_fit["remaining"] = best_fit["length"]

    total_waste = sum(
        material["remaining"] for material in materials if material["quantity"] > 0
    )
    waste_ratio = (
        total_waste / sum(length * quantity for length, quantity in original_materials)
    ) * 100

    summary = {
        "used_materials": used_materials,
        "total_waste": total_waste,
        "waste_ratio": waste_ratio,
    }

    return summary


original_materials = [(10, 100), (20, 300), (30, 200)]
cut_specifications = [(5, 100), (10, 200), (15, 300)]

bfd_summary_with_details = best_fit_decreasing_with_cut_details(
    original_materials, cut_specifications
)

formatted_output_with_details = (
    f"Total Waste: {bfd_summary_with_details['total_waste']}\n"
)
formatted_output_with_details += (
    f"Waste Ratio: {bfd_summary_with_details['waste_ratio']:.2f}%\n"
)
for length, details in bfd_summary_with_details["used_materials"].items():
    formatted_output_with_details += f"Length: {length}, Used: {details['used']}, Cut Details: {details['cut_details']}\n"

print(formatted_output_with_details)
