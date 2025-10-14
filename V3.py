import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculadoraRenta:
    """Mini-Aplicación de Simulación de Renta de Trabajo en Colombia usando Tkinter.
    
    NOTA IMPORTANTE: Se asume la UVT de $49.799 (Año 2024) y se aplica la 
    Renta Exenta Laboral del 25% de forma automática (Art. 206, Num. 10 E.T.).
    """

    def __init__(self, master):
        self.master = master
        master.title("Simulador de Renta Laboral 🇨🇴")
        master.resizable(False, False)

        # Constante UVT para el año de declaración (2024 para declarar en 2025)
        self.UVT = 49799

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'))

        # Variables de entrada (usando snake_case para consistencia)
        self.ingresos_brutos = tk.DoubleVar(value=0.0)
        self.aportes_obligatorios = tk.DoubleVar(value=0.0)
        self.total_retenciones = tk.DoubleVar(value=0.0)
        self.impuesto_neto_anterior = tk.DoubleVar(value=0.0)
        self.otras_deducciones = tk.DoubleVar(value=0.0) # Añadido para otras deducciones/rentas exentas
        self.anio_declaracion = tk.StringVar(value="1")
        
        # Diccionario de ayuda para guiar al usuario
        self.help_messages = {
            1: ("1. Total de Ingresos Laborales ($)", 
                "Ingresa la suma de todos tus ingresos brutos (salario, honorarios, etc.) del año a declarar.",
                "Ejemplo: Si ganaste $80'000.000, ingresa 80000000."),
            2: ("2. Aportes Obligatorios (Salud/Pensión) ($)", 
                "Ingresa el total que aportaste obligatoriamente a salud y pensión durante el año fiscal.",
                "Ejemplo: 8% del IBC. Ingresa 7200000."),
            3: ("3. Otras Deducciones/Rentas Exentas ($)", 
                "Ingresa la suma de otras deducciones (medicina prepagada, intereses de vivienda, dependientes) que califiquen.",
                "Ejemplo: Si tienes dependientes y medicina prepagada, ingresa 10000000."),
            4: ("4. Total Retenciones Practicadas ($)", 
                "Ingresa el total que tu empleador te retuvo en la fuente por concepto de impuesto de renta.",
                "Ejemplo: Si tus certificados indican $500.000 en retenciones, ingresa 500000."),
            5: ("5. Impuesto Neto del Año Anterior ($)", 
                "Ingresa el valor del 'Impuesto Neto de Renta' que pagaste en tu declaración del año pasado (si aplica).",
                "Ejemplo: Si tu impuesto neto anterior fue $1'500.000, ingresa 1500000."),
            6: ("6. Veces que ha Declarado Renta", 
                "Selecciona cuántas veces has presentado declaración de renta, ya que esto afecta el cálculo del Anticipo.",
                "Opciones: 1, 2, o 3+ veces.")
        }

        # Configuración de la Interfaz
        self.create_widgets()
        
    def show_help(self, step):
        """Actualiza el panel de ayuda con la información del paso actual."""
        if step == 0:
            title = "¡Bienvenido al Simulador de Renta!"
            desc = "Haz clic o navega con la tecla Tab a cualquier campo de entrada (1 a 6) para ver su explicación y un ejemplo de lo que debes ingresar."
            example = ""
        else:
            title, desc, example = self.help_messages.get(step, ("", "Campo no encontrado.", ""))
        
        self.help_title_label.config(text=f"{title}")
        self.help_desc_label.config(text=f"{desc}\n\n{example}")


    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.master, padding="15 15 15 15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # --- Sección de Entradas ---

        # 1. Ingresos Laborales
        ttk.Label(main_frame, text="1. Total de Ingresos Laborales ($):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ingresos_entry = ttk.Entry(main_frame, textvariable=self.ingresos_brutos, width=25, justify='right')
        self.ingresos_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.ingresos_entry.bind('<FocusIn>', lambda e: self.show_help(1))

        # 2. Aportes Obligatorios (Salud/Pensión)
        ttk.Label(main_frame, text="2. Aportes Obligatorios (Salud/Pensión) ($):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.aportes_entry = ttk.Entry(main_frame, textvariable=self.aportes_obligatorios, width=25, justify='right')
        self.aportes_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        self.aportes_entry.bind('<FocusIn>', lambda e: self.show_help(2))
        
        # 3. Otras Rentas Exentas o Deducciones (Med. Prepagada, Dependientes, etc.)
        ttk.Label(main_frame, text="3. Otras Deducciones/Rentas Exentas ($):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.otras_deducciones_entry = ttk.Entry(main_frame, textvariable=self.otras_deducciones, width=25, justify='right')
        self.otras_deducciones_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        self.otras_deducciones_entry.bind('<FocusIn>', lambda e: self.show_help(3))

        # 4. Retenciones en la Fuente
        ttk.Label(main_frame, text="4. Total Retenciones Practicadas ($):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.retenciones_entry = ttk.Entry(main_frame, textvariable=self.total_retenciones, width=25, justify='right')
        self.retenciones_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        self.retenciones_entry.bind('<FocusIn>', lambda e: self.show_help(4))

        # 5. Impuesto Neto Año Anterior (Para Anticipo)
        ttk.Label(main_frame, text="5. Impuesto Neto del Año Anterior ($):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.impuesto_anterior_entry = ttk.Entry(main_frame, textvariable=self.impuesto_neto_anterior, width=25, justify='right')
        self.impuesto_anterior_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
        self.impuesto_anterior_entry.bind('<FocusIn>', lambda e: self.show_help(5))

        # 6. Veces que ha Declarado Renta
        ttk.Label(main_frame, text="6. Veces que ha Declarado Renta:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        opciones_declaracion = ["1", "2", "3+"]
        self.declaracion_menu = ttk.Combobox(main_frame, textvariable=self.anio_declaracion, values=opciones_declaracion, state="readonly", width=23)
        self.declaracion_menu.grid(row=5, column=1, padx=5, pady=5, sticky=tk.E)
        self.declaracion_menu.current(0)
        self.declaracion_menu.bind('<FocusIn>', lambda e: self.show_help(6))


        # Botón de Cálculo
        self.calc_button = ttk.Button(main_frame, text="Calcular Impuesto y Anticipo", command=self.calcular, style='TButton')
        self.calc_button.grid(row=6, column=0, columnspan=2, pady=15)
        
        # --- Panel de Instrucciones Dinámicas ---
        help_frame = ttk.LabelFrame(main_frame, text="Instrucciones y Ejemplo", padding="10 10 10 10")
        help_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=10)
        
        self.help_title_label = ttk.Label(help_frame, text="", font=('Helvetica', 10, 'bold'), foreground='darkgreen', wraplength=400)
        self.help_title_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.help_desc_label = ttk.Label(help_frame, text="", wraplength=400)
        self.help_desc_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Inicializar el mensaje de bienvenida
        self.show_help(0)

        # --- Sección de Resultados ---
        
        results_frame = ttk.LabelFrame(main_frame, text="Resultados de la Simulación", padding="10 5")
        results_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 1. Impuesto Bruto Calculado
        ttk.Label(results_frame, text="Impuesto Bruto Calculado:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.impuesto_bruto_label = ttk.Label(results_frame, text="$ 0", foreground="blue", font=('Helvetica', 10, 'bold'))
        self.impuesto_bruto_label.grid(row=0, column=1, padx=5, pady=2, sticky=tk.E)

        # 2. Saldo Final a Pagar/Favor
        ttk.Label(results_frame, text="Saldo Final (Impuesto + Anticipo - Retenciones):").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.saldo_final_label = ttk.Label(results_frame, text="$ 0", foreground="blue", font=('Helvetica', 10, 'bold'))
        self.saldo_final_label.grid(row=1, column=1, padx=5, pady=2, sticky=tk.E)

        # 3. Anticipo Requerido
        ttk.Label(results_frame, text="Anticipo Requerido para el Próximo Año:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.anticipo_final_label = ttk.Label(results_frame, text="$ 0", foreground="green", font=('Helvetica', 10, 'bold'))
        self.anticipo_final_label.grid(row=2, column=1, padx=5, pady=2, sticky=tk.E)

    def format_currency(self, value):
        """Formatea un número a formato de moneda con separadores de miles (formato colombiano)."""
        if value is None:
            return "$ 0"
        # Usamos el formato local de Python y luego ajustamos:
        # 1. Reemplazamos el separador de miles (,) por un punto (.).
        # 2. Reemplazamos el punto decimal (.) por una coma (,).
        # 3. Finalmente, se quita el separador decimal si el resultado es entero.
        formatted = f"{value:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".")
        return f"$ {formatted}"

    def calcular_impuesto_241(self, base_gravable_uvt):
        """Aplica la Tabla de Tarifas Progresivas del Art. 241 E.T. (Impuesto en UVT)."""
        base_gravable_uvt = math.floor(base_gravable_uvt) # La base gravable se redondea al entero inferior

        if base_gravable_uvt <= 1090:
            return 0.0
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
            # 1. Lectura y validación de Entradas (usando snake_case)
            ingresos_brutos = self.ingresos_brutos.get()
            aportes_obligatorios = self.aportes_obligatorios.get()
            total_retenciones = self.total_retenciones.get()
            impuesto_neto_anterior = self.impuesto_neto_anterior.get()
            otras_deducciones = self.otras_deducciones.get()
            anio_declaracion = self.anio_declaracion.get()

            if any(val < 0 for val in [ingresos_brutos, aportes_obligatorios, total_retenciones, impuesto_neto_anterior, otras_deducciones]):
                 raise ValueError("Todos los valores de entrada deben ser positivos o cero.")
            
            # El aporte obligatorio no puede ser mayor al ingreso
            if aportes_obligatorios > ingresos_brutos:
                raise ValueError("Los aportes obligatorios no pueden superar los ingresos brutos.")

        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Asegúrese de ingresar números válidos. {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            return

        # 2. MÓDULO DE DEPURACIÓN (Art. 336 E.T.)

        # Renta líquida antes de rentas exentas y deducciones
        renta_liquida_ordinaria = max(0, ingresos_brutos - aportes_obligatorios)

        # 2.1. Renta Exenta Laboral (25% sobre la Renta Líquida)
        # Límite: 2400 UVT anuales (2400 * 49799 = $119,517,600)
        renta_exenta_25_pct = renta_liquida_ordinaria * 0.25
        renta_exenta_25_pct = min(renta_exenta_25_pct, 2400 * self.UVT)

        # Total de Rentas Exentas y Deducciones (sujetas a límite)
        total_exenciones_deducciones = renta_exenta_25_pct + otras_deducciones
        
        # 2.2. Límite del 40% (Tope General)
        tope_40_pct = renta_liquida_ordinaria * 0.40
        tope_1340_uvt = self.UVT * 1340 

        # Las deducciones permitidas se limitan al menor de los topes
        limite_deducciones = min(tope_40_pct, tope_1340_uvt)
        
        # Deducción Final Aplicable:
        deducciones_permitidas = min(total_exenciones_deducciones, limite_deducciones)

        # Base Gravable (Renta Líquida - Deducciones Permitidas)
        base_gravable = max(0, renta_liquida_ordinaria - deducciones_permitidas)

        # 3. MÓDULO DE CÁLCULO DEL IMPUESTO (Art. 241 E.T.)
        
        base_gravable_uvt = base_gravable / self.UVT
        
        # Impuesto Bruto en UVT (aplicando la tabla)
        impuesto_bruto_uvt = self.calcular_impuesto_241(base_gravable_uvt)
        
        # Impuesto Bruto en pesos
        impuesto_bruto_pesos = impuesto_bruto_uvt * self.UVT
        
        # Impuesto Neto (lo que debe pagar antes de anticipos)
        impuesto_neto_actual = max(0, impuesto_bruto_pesos - total_retenciones)
        
        # 4. MÓDULO DE ANTICIPO (Art. 807 E.T.)

        # Definir Porcentaje basado en Anio_Declaracion
        if anio_declaracion == "1":
            porcentaje = 0.25
        elif anio_declaracion == "2":
            porcentaje = 0.50
        else: # "3+"
            porcentaje = 0.75

        # Método 1: Impuesto Actual
        anticipo_metodo1 = max(0, (impuesto_bruto_pesos * porcentaje) - total_retenciones)

        # Método 2: Promedio de los dos últimos años 
        if impuesto_neto_anterior > 0 or impuesto_bruto_pesos > 0:
             promedio = (impuesto_bruto_pesos + impuesto_neto_anterior) / 2
        else:
            promedio = 0 

        anticipo_metodo2 = max(0, (promedio * porcentaje) - total_retenciones)
        
        # Anticipo Final es el menor de los dos métodos
        anticipo_final = min(anticipo_metodo1, anticipo_metodo2)
        
        # 5. Saldo Final 
        # Saldo Final a Pagar/Favor = Impuesto Bruto - Retenciones - Anticipo Año Anterior + Anticipo Año Siguiente
        saldo_final_pagar_favor = impuesto_bruto_pesos - total_retenciones + anticipo_final
        
        # 6. Presentación de Resultados
        self.impuesto_bruto_label.config(text=self.format_currency(round(impuesto_bruto_pesos)))
        
        # Ajustar color para Saldo Final
        saldo_color = "red" if saldo_final_pagar_favor > 0 else "blue"
        self.saldo_final_label.config(text=self.format_currency(round(saldo_final_pagar_favor)), foreground=saldo_color)
        
        self.anticipo_final_label.config(text=self.format_currency(round(anticipo_final)))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraRenta(root)
    root.mainloop()