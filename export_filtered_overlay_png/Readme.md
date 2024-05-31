# Export Filtered Overlay Scripts
Those scripts are used for exporting the filtered overlay. The filtered overlay images are created by the script "crack2curve.py".
- "export_filtered_overlay_png.py": export the filtered overlay png, but the result image size is too large.
- "copy_and_resize.py": resize "filtered_overlay.png" from the curve folder and place the results into nn_filtered_crack_overlay folder;
- "copy_and_resize_parallel.py": this file used parallel processing to make the processing faster.
- "export_nn_filtered_mask.py": export the filtered mask, those masks may be used by the front end.
- "export_solid_filtered_overlay.py": export the solid filtered overlay. Those files are used by the WebODM for 3D reconstruction.