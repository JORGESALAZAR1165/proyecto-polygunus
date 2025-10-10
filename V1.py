import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculadoraRenta:
    """Mini-Aplicación de Simulación de Renta de Trabajo en Colombia usando Tkinter."""

    def __init__(self, master):
        self.master = master
        master.title("Simulador de Renta (Trabajo) 🇨🇴")
        master.resizable(False, False)

        # Constante Dura
        self.UVT = 49799

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'))

        # Variables de entrada
        self.ingresos_brutos = tk.DoubleVar()
        self.aportes_obligatorios = tk.DoubleVar()
        self.total_retenciones = tk.DoubleVar()
        self.impuesto_neto_anterior = tk.DoubleVar()
        self.anio_declaracion = tk.StringVar(value="1")

        # Configuración de la Interfaz
        self.create_widgets()

    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # --- Sección de Entradas ---

        # 1. Ingresos Laborales
        ttk.Label(main_frame, text="Total de Ingresos Laborales ($):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ingresos_entry = ttk.Entry(main_frame, textvariable=self.ingresos_brutos, width=25)
        self.ingresos_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        # 2. Aportes Obligatorios (Salud/Pensión)
        ttk.Label(main_frame, text="Aportes Obligatorios (Salud/Pensión) ($):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.aportes_entry = ttk.Entry(main_frame, textvariable=self.aportes_obligatorios, width=25)
        self.aportes_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

        # 3. Retenciones en la Fuente
        ttk.Label(main_frame, text="Total Retenciones Practicadas ($):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.retenciones_entry = ttk.Entry(main_frame, textvariable=self.total_retenciones, width=25)
        self.retenciones_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

        # 4. Impuesto Neto Año Anterior (Para Anticipo)
        ttk.Label(main_frame, text="Impuesto Neto del Año Anterior ($):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.impuesto_anterior_entry = ttk.Entry(main_frame, textvariable=self.impuesto_neto_anterior, width=25)
        self.impuesto_anterior_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

        # 5. Veces que ha Declarado Renta
        ttk.Label(main_frame, text="Veces que ha Declarado Renta:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        opciones_declaracion = ["1", "2", "3+"]
        self.declaracion_menu = ttk.Combobox(main_frame, textvariable=self.anio_declaracion, values=opciones_declaracion, state="readonly", width=23)
        self.declaracion_menu.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
        self.declaracion_menu.current(0)

        # Botón de Cálculo
        self.calc_button = ttk.Button(main_frame, text="Calcular Impuesto y Anticipo", command=self.calcular)
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=15)

        # --- Sección de Resultados ---
        
        results_frame = ttk.LabelFrame(main_frame, text="Resultados de la Simulación", padding="10 5")
        results_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 1. Impuesto Bruto Calculado
        ttk.Label(results_frame, text="Impuesto Bruto Calculado:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.impuesto_bruto_label = ttk.Label(results_frame, text="$ 0", foreground="blue", font=('Helvetica', 10, 'bold'))
        self.impuesto_bruto_label.grid(row=0, column=1, padx=5, pady=2, sticky=tk.E)

        # 2. Saldo Final a Pagar/Favor
        ttk.Label(results_frame, text="Saldo Final a Pagar/Favor:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.saldo_final_label = ttk.Label(results_frame, text="$ 0", foreground="blue", font=('Helvetica', 10, 'bold'))
        self.saldo_final_label.grid(row=1, column=1, padx=5, pady=2, sticky=tk.E)

        # 3. Anticipo Requerido
        ttk.Label(results_frame, text="Anticipo Requerido para el Próximo Año:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.anticipo_final_label = ttk.Label(results_frame, text="$ 0", foreground="green", font=('Helvetica', 10, 'bold'))
        self.anticipo_final_label.grid(row=2, column=1, padx=5, pady=2, sticky=tk.E)

        # Inicializar todos los inputs a 0.0 para evitar errores si están vacíos al inicio
        self.ingresos_brutos.set(0.0)
        self.aportes_obligatorios.set(0.0)
        self.total_retenciones.set(0.0)
        self.impuesto_neto_anterior.set(0.0)

    def format_currency(self, value):
        """Formatea un número a formato de moneda con separadores de miles."""
        return f"$ {value:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".") # Formato colombiano

    def calcular_impuesto_241(self, base_gravable_uvt):
        """Aplica la Tabla de Tarifas Progresivas del Art. 241 E.T."""
        if base_gravable_uvt <= 1090:
            return 0
        elif base_gravable_uvt <= 1630:
            exceso = base_gravable_uvt - 1090
            return (exceso * 0.19)
        elif base_gravable_uvt <= 4190:
            exceso = base_gravable_uvt - 1630
            return (103 + exceso * 0.28)
        elif base_gravable_uvt <= 8670:
            exceso = base_gravable_uvt - 4190
            return (828 + exceso * 0.33)
        elif base_gravable_uvt <= 18970:
            exceso = base_gravable_uvt - 8670
            return (2270 + exceso * 0.35)
        elif base_gravable_uvt <= 32370:
            exceso = base_gravable_uvt - 18970
            return (5890 + exceso * 0.37)
        else: # Mayor a 32370
            exceso = base_gravable_uvt - 32370
            return (10954 + exceso * 0.39)

    def calcular(self):
        try:
            # 1. Lectura y validación de Entradas
            IngresosBrutos = self.ingresos_brutos.get()
            AportesObligatorios = self.aportes_obligatorios.get()
            TotalRetenciones = self.total_retenciones.get()
            Impuesto_Neto_Anterior = self.impuesto_neto_anterior.get()
            Anio_Declaracion = self.anio_declaracion.get()

            if any(val < 0 for val in [IngresosBrutos, AportesObligatorios, TotalRetenciones, Impuesto_Neto_Anterior]):
                 raise ValueError("Todos los valores deben ser positivos o cero.")

        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Asegúrese de ingresar números válidos. {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            return

        # 2. MÓDULO DE DEPURACIÓN (Art. 336 E.T.)

        DeduccionesOblig = AportesObligatorios
        Tope40 = IngresosBrutos * 0.40
        TopeUVT = self.UVT * 1340 # Tope general de 1340 UVT
        
        # Las deducciones permitidas se limitan al menor de los topes
        DeduccionesPermitidas = min(DeduccionesOblig, Tope40, TopeUVT)
        
        # La base gravable se calcula después de aplicar las deducciones
        BaseGravable = max(0, IngresosBrutos - DeduccionesPermitidas)

        # 3. MÓDULO DE CÁLCULO DEL IMPUESTO (Art. 241 E.T.)
        
        BaseGravable_UVT = BaseGravable / self.UVT
        
        # Impuesto Bruto en UVT (aplicando la tabla)
        ImpuestoBruto_UVT = self.calcular_impuesto_241(BaseGravable_UVT)
        
        # Impuesto Bruto en pesos
        ImpuestoBruto_Pesos = ImpuestoBruto_UVT * self.UVT
        
        # Impuesto Neto (lo que debe pagar antes de anticipos)
        ImpuestoNetoActual = ImpuestoBruto_Pesos - TotalRetenciones
        
        # Saldo Final a Pagar/Favor
        # Si ImpuestoNetoActual es positivo, es Saldo a Pagar. Si es negativo, es Saldo a Favor.
        Saldo_Final_Pagar_Favor = ImpuestoNetoActual
        
        # 4. MÓDULO DE ANTICIPO (Art. 807 E.T.)

        # Definir Porcentaje basado en Anio_Declaracion
        if Anio_Declaracion == "1":
            Porcentaje = 0.25
        elif Anio_Declaracion == "2":
            Porcentaje = 0.50
        else: # "3+"
            Porcentaje = 0.75

        # Método 1: Impuesto Actual
        Anticipo_Metodo1 = max(0, (ImpuestoBruto_Pesos * Porcentaje) - TotalRetenciones)

        # Método 2: Promedio de los dos últimos años (solo si hay año anterior)
        if Impuesto_Neto_Anterior > 0 or ImpuestoBruto_Pesos > 0:
            Promedio = (ImpuestoBruto_Pesos + Impuesto_Neto_Anterior) / 2
        else:
            Promedio = 0 # No tiene sentido promediar si ambos son cero o negativos.

        Anticipo_Metodo2 = max(0, (Promedio * Porcentaje) - TotalRetenciones)
        
        # Anticipo Final es el menor de los dos métodos
        Anticipo_Final = min(Anticipo_Metodo1, Anticipo_Metodo2)

        # 5. Presentación de Resultados
        self.impuesto_bruto_label.config(text=self.format_currency(round(ImpuestoBruto_Pesos)))
        
        # Ajustar color para Saldo Final
        saldo_color = "red" if Saldo_Final_Pagar_Favor > 0 else "blue"
        self.saldo_final_label.config(text=self.format_currency(round(Saldo_Final_Pagar_Favor)), foreground=saldo_color)
        
        self.anticipo_final_label.config(text=self.format_currency(round(Anticipo_Final)))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraRenta(root)
    root.mainloop()

