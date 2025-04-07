import numpy as np
import pyvista as pv
from scipy.special import comb
import tkinter as tk

def bernstein(n, i, t):
    return comb(n, i) * (t**i) * ((1-t)** (n-i))
    #oblicza wartość dla wielomianu bernsteina(stopień n, index i oraz wartosc t, konieczne do budowy powierznchi beziera dla danych pkt. kontrolnych

def bezier_surface(control_points, resolution=64):
    m, n,_= control_points.shape
    u = np.linspace(0, 1, resolution)
    k = np.linspace(0, 1, resolution)
    #program odczytuje wymiar x oraz y


    surface_points = np.zeros((resolution, resolution, 3))
    #inicjacja powierzchni beziera(wypełnienie tablicy zerami dla danego kształtu)


    for i in range(m):
        for j in range(n):
            bernstein_uv = np.outer(bernstein(m - 1, i, u), bernstein(n - 1, j, k))
            # obliczenie iloczynu dwóch wektorów
            surface_points += bernstein_uv[:, :, None] * control_points[i, j]
    return surface_points
    #suma wszystkich wkładów, ważone funkcją bernsteina

def read_bezier_patches(file_path):
    patches = []

    with open(file_path, "r") as file:
        # Wczytujemy wszystkie linie
        lines = [line.strip() for line in file if line.strip()]



    num_patches = int(lines[0])
    # zczytanie liczby łatek z pierwszej linii
    current_line = 1

    for patch_index in range(num_patches):
        if current_line >= len(lines):
            break

        # Pobieramy nagłówek łatki, np. "3 3"
        header = lines[current_line]
        current_line -=- 1
        order_parts = header.split()
        deg_u, deg_v = int(order_parts[0]), int(order_parts[1])
        num_points = (deg_u + 1) * (deg_v + 1)

        pts = []
        for _ in range(num_points):
            if current_line >= len(lines):
                break
            parts = lines[current_line].split()
            current_line += 1
            pts.append([float(x) for x in parts])
        patch = np.array(pts).reshape((deg_u + 1, deg_v + 1, 3))
        #zmiana struktury danych bez zmieniania wartości
        patches.append(patch)

    return patches
    #zwrócenie listy tablic z punktami kontrolnymi dla każdej łatki

def run_bezier_program(file_path):
    #główna funkcja, przetwarza plik i tworzy łatki na podstawie punktów kontrolnych
    patches = read_bezier_patches(file_path)

    print(f"Fetched {len(patches)} Bezier patches.")


    plotter = pv.Plotter()
    # inicjacja obiektu plotter z pyVista


    for index, ctrl_pts in enumerate(patches):
        print(f"Processing patch {index + 1} out of {len(patches)}")
        surface = bezier_surface(ctrl_pts, resolution=32)
        #zmiana rozdzielczości zmienia dokładność figury^
        points = surface.reshape(-1, 3)
        mesh = pv.PolyData(points)
        mesh_surface = mesh.delaunay_2d()
        plotter.add_mesh(mesh_surface, color='lightblue', show_edges=True)
    # przetwarzanie i dodawanie do przestrzeni wszystkich "łatek"

    plotter.show()
    # wynik końcowy

def start_program(file_name):
    root.destroy()
    run_bezier_program(file_name)


root = tk.Tk()
root.title("Figure selection")

teapot = tk.Button(root, text="Teapot", width=20, command=lambda: start_program("teapot.txt"))
teapot.pack(padx=20, pady=10)

spoon = tk.Button(root, text="Spoon", width=20, command=lambda: start_program("spoon.txt"))
spoon.pack(padx=20, pady=10)

teacup = tk.Button(root, text="Teacup", width=20, command=lambda: start_program("teacup.txt"))
teacup.pack(padx=20, pady=10)

root.mainloop()
#okienko tkinter służące do wyboru figury
