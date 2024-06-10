# from litologias import *
# from PaletadeCores import *
import numpy as np
import pandas as pd
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import colorchooser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import copy
import json


# pip install openpyxl


def Abrir_paleta():
    global filepath_palet, lithologies_name
    filepath_palet = filedialog.askopenfilename(
        initialdir="C:\\Users\\brbru\Desktop\\Programacao\\Tkinter_py",
        title="Abrir Paletas:",
        filetypes=(("json", "*.json"), ("all files", "*.*")),
    )

    # openPalet=True
    with open(filepath_palet, "r") as arquivo_json:
        dic = json.load(arquivo_json)
    lithologies_name = dic
    return lithologies_name


def intervalo(prof):
    # dá o espaçamento entre as amostras
    df = pd.DataFrame(prof, columns=["prof"])
    pf = []
    p = []
    c = 0
    # trocar esse set por uma função que remova duplicatas!!!!!!
    for i in df.prof.unique():
        pf.append(i)
        if len(pf) == 2:
            p.append(pf[-1] - pf[0 + c])
            p.append(pf[-1] - pf[0 + c])
        elif len(pf) > 2:
            p.append(pf[-1] - pf[1 + c])
            c += 1
    d = {pf[0]: p[0]}
    for i in range(1, len(p)):
        d[pf[i]] = p[i]
    return d


def porcentagem(porcentagem):
    if porcentagem in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        return int(porcentagem)
    else:
        return 0


def cod_shortname(mnemonico):
    if mnemonico.upper() in lithologies_name.keys():
        return mnemonico.upper()
    else:
        print("mnemonico não identificado:", mnemonico)


def granulometria(x, y=np.nan):
    if x in [
        "AND",
        "BAS",
        "ARS",
        "CRN",
        "CRV",
        "CHT",
        "CIM",
        "DIA",
        "GIP",
        "GNA",
        "GRN",
        "HAL",
        "INI",
        "IGB",
        "MSD",
        "SNI",
        "SLX",
        "TQD",
        "CLC",
    ]:
        return 0
    elif x in ["CAL"]:
        return 1.5
    elif x in ["GRS", "CRE"]:
        return 5
    elif x in ["PKS"]:
        return 4
    elif x in ["MDS"]:
        return 2
    elif x in ["WKS"]:
        return 3
    elif x in [
        "ARG",
        "AGT",
        "AGN",
        "AGL",
        "AGC",
        "AGB",
        "CLU",
        "FLH",
        "MRG",
        "ESF",
        "LMT",
    ]:
        return 1
    elif x in ["AGS", "CSI", "FLS", "SLT"]:
        return 2
    elif x in ["ARO", "CRU", "CGL", "COQ", "DMT", "BRC", "BRV", "BLT", "CRU"]:
        return 5.5

    elif x in ["ARL", "ARC", "ARF", "ART", "ARE", "ARN"]:
        if y == "MFN":
            return 2.5
        elif y == "FNO":
            return 3
        elif y == "MED":
            return 3.5
        elif y == "GRO":
            return 4
        elif y == "MGR":
            return 4.5
        elif y == "CGO":
            return 5
        else:
            return 3.5
    else:
        return 0


def Dados():
    # data=leitura()
    data = pd.read_excel(filepath)
    data = pd.DataFrame(
        np.array(
            [
                data[data.columns[0]],
                data[data.columns[1]],
                data[data.columns[2]],
                data[data.columns[3]],
            ]
        ).T
    )
    data.columns = ["PROF", "LITO", "%", "GRAN"]
    Prof = np.array(data.PROF)
    for i in range(len(Prof)):
        if np.isnan(Prof[i]) != True:
            pass
        else:
            while np.isnan(Prof[i]) == True:
                Prof[i] = Prof[i - 1]
    return Prof, data.LITO, data["%"], data.GRAN


def Order_Lito(a):
    # a=[ar.tolist() for ar in a]
    for i in range(len(a)):
        if a[i][0] in [
            "AGT",
            "AGC",
            "AGL",
            "AGB",
            "ARG",
            "FLH",
            "FLS",
            "MRG",
            "TOL",
            "SLT",
            "AGS",
            "TOS",
            "ARN",
            "ARE",
            "ARL",
            "ARF",
            "ART",
            "ARC",
            "CGL",
            "ARO",
            "BRC",
            "DMT",
            "CAL",
            "CLC",
            "CHT",
            "DOL",
            "CLU",
            "MDS",
            "WKS",
            "CSI",
            "PKS",
            "CRE",
            "GRS",
            "CRU",
            "COQ",
            "BLT",
        ]:
            if a[i][0] in ["AGT", "AGC", "AGL", "AGB", "ARG"]:  # Argilas
                a[i].append(1)
            if a[i][0] in ["FLH", "FLS", "MRG", "TOL"]:  # Folhelhos
                a[i].append(2)
            if a[i][0] in ["SLT", "AGS", "TOS"]:  # siltes
                a[i].append(3)
            if a[i][0] in ["ARN", "ARE", "ARL", "ARF", "ART", "ARC"]:  # areias
                a[i].append(4)
            if a[i][0] in ["CGL", "ARO", "BRC", "DMT"]:
                a[i].append(5)
            if a[i][0] in ["CAL", "CLC", "CHT", "DOL"]:  # calcario
                a[i].append(6)
            if a[i][0] in ["CLU", "MDS"]:  # Cal argilitO
                a[i].append(7)
            if a[i][0] in ["WKS"]:
                a[i].append(7.5)
            if a[i][0] in ["CSI", "PKS"]:  # Cal siltito
                a[i].append(8)
            if a[i][0] in ["CRE", "GRS"]:  # Cal arenito
                a[i].append(9)
            if a[i][0] in ["CRU", "COQ", "BLT"]:  # Cal rudito
                a[i].append(10)
        else:
            a[i].append(999)
    a = sorted(a, key=lambda x: x[2])
    return a


def Sum_Lit(x):
    # Somas as porcentagem das litologias semelhantes
    for i in range(len(x)):
        A = x[i][0]

        for j in range(len(x)):
            if i != j:
                if A == x[j][0]:
                    x[j][1] = int(x[i][1]) + int(x[j][1])
                    x[i][1] = 0
    return x


def litodic():
    prof = Dados()[0]
    lit = Dados()[1]
    perc = Dados()[2]
    granu = Dados()[3]
    d = intervalo(prof)
    l = {
        prof[0]: {
            "Lito": [[cod_shortname(lit[0]), porcentagem(perc[0])]],
            "Espacamento": d[prof[0]],
            "Granulometria": granulometria(cod_shortname(lit[0]), granu[0]),
        }
    }
    g = [[cod_shortname(lit[0]), porcentagem(perc[0]), granu[0]]]  #
    gnm = {}  #
    for i in range(1, len(prof)):
        if prof[i] in l:
            if prof[i] == prof[i - 1]:
                l[prof[i]]["Lito"].append([cod_shortname(lit[i]), porcentagem(perc[i])])
                g.append([cod_shortname(lit[i]), porcentagem(perc[i]), granu[i]])
        else:
            g = Sum_Lit(g)
            g = sorted(g, key=lambda x: int(x[1]), reverse=True)
            gnm[prof[i - 1]] = [g[0][0], granulometria(g[0][0], g[0][2])]
            g = []
            g.append([cod_shortname(lit[i]), porcentagem(perc[i]), granu[i]])
            dic = {
                "Lito": [[cod_shortname(lit[i]), porcentagem(perc[i])]],
                "Espacamento": d[prof[i]],
                "Granulometria": granulometria(cod_shortname(lit[i]), granu[i]),
            }
            l[prof[i]] = dic

    g = Sum_Lit(g)
    g = sorted(g, key=lambda x: int(x[1]), reverse=True)
    gnm[prof[i]] = [g[0][0], granulometria(g[0][0], g[0][2])]

    return l, gnm


def Array_Prof_Gran(gnm):
    pf = [
        0,
    ]
    gran = []
    litg = []
    for i in gnm.keys():
        pf.append(i)
        gran.append(gnm[i][1])
        litg.append(gnm[i][0])
    pf[0] = pf[1] - (pf[2] - pf[1])
    return np.array(pf), np.array(litg), np.array(gran)


def funcgran(e, u, o):
    # e-prof
    # u-granulo
    h = []  # prof
    j = []  # granulo
    k = []

    for i in range(len(e) - 1):
        if i == 0:
            h.append(e[i + 1] - (e[i + 1] - e[i]))
            h.append(e[i])
            j.append(u[i])
            j.append(u[i])
            k.append(o[i])
            k.append(o[i])
        else:
            j.append(u[i])
            h.append(e[i])
            k.append(o[i])
    j.append(u[-1])
    h.append(e[-1])
    k.append(o[-1])
    return h, j, k


def JanelaGrafico():
    def ax_graphyc(N, l, axis=0):
        pass
        """lim=100
    alp=0.8
    prof=np.arange(N-l[N]["Espacamento"],N+1,1)
    a=(l[N]["Lito"][0][1]/100)*lim
    ax[axis].fill_betweenx(prof,a, facecolor=str(lithologies_num[l[N]["Lito"][0][0]]["patch_property"]['color']),edgecolor='k', alpha=alp,linewidth=0.2)
    l[N]["Lito"]
    for i in range(1,len(l[N]["Lito"])):
      if np.isnan(l[N]["Lito"][i][0])==False:
        b=(l[N]["Lito"][i][1]/100)*lim+a
        ax[axis].fill_betweenx(prof,b,a,facecolor=str(lithologies_num[l[N]["Lito"][i][0]]["patch_property"]['color']),edgecolor='k', alpha=alp,linewidth=0.2)
        a=b"""

    def graphyc(N, L):
        lim = 100
        alp = 1
        l = copy.deepcopy(L)
        l[N]["Lito"] = Order_Lito(l[N]["Lito"])
        prof = np.arange(N - l[N]["Espacamento"], N + 1, 1)
        a = (l[N]["Lito"][0][1] / 100) * lim
        plt.fill_betweenx(
            prof,
            a,
            facecolor=str(
                lithologies_name[l[N]["Lito"][0][0]]["patch_property"]["color"]
            ),
            hatch=str(lithologies_name[l[N]["Lito"][0][0]]["patch_property"]["hatch"]),
            alpha=alp,
            linewidth=0.2,
        )
        for i in range(1, len(l[N]["Lito"])):
            if (l[N]["Lito"][i][1]) != "":  # TROCAR
                b = (l[N]["Lito"][i][1] / 100) * lim + a
                plt.fill_betweenx(
                    prof,
                    b,
                    a,
                    facecolor=str(
                        lithologies_name[l[N]["Lito"][i][0]]["patch_property"]["color"]
                    ),
                    hatch=str(
                        lithologies_name[l[N]["Lito"][i][0]]["patch_property"]["hatch"]
                    ),
                    alpha=alp,
                    linewidth=0.2,
                )
                a = b

    def sedlog(l, axis=False, axis_n=0):
        if axis == False:
            for N in l.keys():
                graphyc(N, l)
        else:
            for N in l.keys():
                ax_graphyc(N, l, axis=axis_n)

    def plotGranulometria(gnm):
        fontsize = 14
        pfmin, pfmax = ProfMaxMin(gnm)
        Profundidade, LitologiasG, Granulometria = Array_Prof_Gran(gnm)
        g = funcgran(Profundidade, Granulometria, LitologiasG)
        for i in range(1, len(Profundidade) - 1):
            plt.fill_between(
                [-1, g[1][i]],
                Profundidade[i - 1],
                Profundidade[i],
                facecolor=lithologies_name[g[2][i]]["patch_property"]["color"],
                hatch=lithologies_name[g[2][i]]["patch_property"]["hatch"],
                alpha=1,
            )
        plt.fill_between(
            [-1, g[1][-1]],
            Profundidade[-1],
            Profundidade[-2],
            facecolor=lithologies_name[g[2][-1]]["patch_property"]["color"],
            hatch=lithologies_name[g[2][-1]]["patch_property"]["hatch"],
            alpha=1,
        )
        plt.step(g[1], g[0], where="pre", color="k")
        plt.title("Granulometria", fontsize=pfontsize + 2, weight=700)

        plt.grid(color="black", linewidth=0.5, alpha=0.8)
        # plt.minorticks_on()
        # plt.grid(axis='y',color='grey', linewidth=0.1, which='minor',alpha=0.0)
        plt.tick_params(labelsize=15, axis="both")
        plt.ylim(float(pfmin), float(pfmax))
        plt.gca().invert_yaxis()
        plt.xlim(-1, 6)
        carscale = False
        if carscale != True:
            plt.xticks(
                [1, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5],
                [
                    "Clay",
                    "Silt",
                    "\nvf",
                    "\nf",
                    "  Sand \nm",
                    "\nc",
                    "\nvc",
                    "\n   gran",
                    "Gravel",
                ],
            )
            plt.xlabel("Granulometria", fontsize=fontsize, weight=600)
        elif carscale == True:
            plt.xticks([2, 3, 4, 5, 6], ["Mud", "Wack", "Pack", "Grain", "Rud"])
            plt.xlabel("\nGranulometria", fontsize=fontsize, weight=600)

    def ProfMaxMin(l):
        pfmin = pmin.get()
        pfmax = pmax.get()
        dif = list(l.keys())[0] - list(l.keys())[1]
        if pfmin == "" and pfmax == "":
            pfmin = list(l.keys())[0] + dif
            pfmax = list(l.keys())[-1]
        elif pfmin == "":
            pfmin = list(l.keys())[0] + dif
            pfmax = pmax.get()
        elif pfmax == "":
            pfmin = pmin.get()
            pfmax = list(l.keys())[-1]
        return pfmin, pfmax

    def plotgraph():
        if filepath == "":
            messagebox.showwarning(title="AVISO", message="Insira o poço.")
        else:
            plotgran = True
            global pfontsize
            pfontsize = 14
            l, gnm = litodic()
            new_window = Tk()
            new_window.title("SedBr - Gráficos")
            # wellname=nome.get()
            pfmin, pfmax = ProfMaxMin(l)
            f = 1
            if plotgran == True:
                f += 1
            fig = plt.figure(figsize=(6 * f + 1, 10))
            global a
            a = 100 + f * 10
            plt.subplot(a + 1)
            # plt.suptitle(wellname.upper(),fontsize=pfontsize+4,weight=800, ha='center', va='baseline')
            plt.title("Descrição", fontsize=pfontsize + 2, weight=700)
            plt.ylabel("Profundidade [m]", fontsize=pfontsize, weight=700)
            plt.xlabel("\nLitologias [%]", fontsize=pfontsize, weight=600)
            sedlog(l)
            plt.ylim(float(pfmin), float(pfmax))
            plt.gca().invert_yaxis()
            plt.xlim(0, 100)
            plt.grid(color="black", linewidth=0.5, alpha=0.8)
            # plt.minorticks_on()
            # plt.grid(axis='y',color='grey', linewidth=0.1, which='minor',alpha=0.5)
            plt.tick_params(labelsize=15, axis="both")
            plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            # plt.tight_layout(pad=10)
            for i in range(10):
                plt.axvline(i * 10, color="gray", linewidth=0.9, linestyle="-")
            if plotgran == True:
                plt.subplot(a + 2)
                plotGranulometria(gnm)
            # plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.get_tk_widget().pack()
            # return plt.show()

    def Quit():
        window.destroy()

    window = Tk()
    window.title("SedBr")
    menubar = Menu(window)
    window.config(menu=menubar)
    # window.iconbitmap(r'sedbricon.ico')
    # Menu arquivo
    filemenu = Menu(menubar, tearoff=0, font=("Arial", 12))
    filemenu2 = Menu(menubar, tearoff=0, font=("Arial", 12))
    menubar.add_cascade(label="Arquivo", menu=filemenu)
    menubar.add_cascade(label="Paletas", menu=filemenu2)
    filemenu.add_command(label="Abrir arquivo", command=Abrir)
    filemenu2.add_command(label="Abrir paleta", command=Abrir_paleta)
    filemenu2.add_command(label="Criar nova paleta", command=Paletas_Criar)

    profmin = Label(window, text="Profundidade Mínima", font=("Arial", 14)).grid(
        row=0, column=0
    )
    pmin = Entry(window, font=("Arial", 14), fg="Blue")
    pmin.grid(row=0, column=1)
    profmax = Label(window, text="Profundidade Máxima", font=("Arial", 14)).grid(
        row=1, column=0
    )
    pmax = Entry(window, font=("Arial", 14), fg="Red")
    pmax.grid(row=1, column=1)
    graph = Button(
        window,
        text="Plot",
        command=plotgraph,
        font=("Comic Sans", 15),
        fg="#DCDCDC",
        bg="black",
        activeforeground="#F8F8FF",
        activebackground="Black",
        width=7,
    )
    graph.grid(row=2, column=1, columnspan=1, pady=7, padx=7, ipadx=100)

    window.mainloop()


def PosicaoCol(nome, data):
    col = np.array(data.columns)
    for i in range(len(col)):
        if col[i] == nome:
            return i


def Abrir():
    def Janela():
        def Salvar():
            HEAD = [Profvar.get(), Litvar.get(), Percvar.get(), Granvar.get()]
            Posicao = [
                PosicaoCol(HEAD[0], data),
                PosicaoCol(HEAD[1], data),
                PosicaoCol(HEAD[2], data),
                PosicaoCol(HEAD[3], data),
            ]
            # print(HEAD,Posicao)
            return HEAD

        def SairSalvar():
            HEAD = [Profvar.get(), Litvar.get(), Percvar.get(), Granvar.get()]
            Posicao = [
                PosicaoCol(HEAD[0], data),
                PosicaoCol(HEAD[1], data),
                PosicaoCol(HEAD[2], data),
                PosicaoCol(HEAD[3], data),
            ]
            # print(HEAD,Posicao)
            window.destroy()
            return HEAD

        window = Toplevel(window1)
        window.grab_set()
        window.title("SedBr - Abrir Arquivo")
        # window.iconbitmap(r'sedbricon.ico')
        if filepath == "":
            pass
        else:
            window.update()
            data = pd.read_excel(filepath)
            col = data.columns
            Litvar = StringVar(window)
            Profvar = StringVar(window)
            Percvar = StringVar(window)
            Granvar = StringVar(window)
            TipV = tuple(data.columns)
            Litvar.set(col[0])
            Profvar.set(col[0])
            Percvar.set(col[0])
            Granvar.set(col[0])
            prof = OptionMenu(window, Profvar, *TipV)
            prof.grid(row=1, column=1)
            proflab = Label(window, text="Profundidade", font=("Arial", 15)).grid(
                row=1, column=0
            )
            Mlit = OptionMenu(window, Litvar, *TipV)
            Mlit.grid(row=2, column=1)
            # Litvar.trace_add('write')
            litolab = Label(window, text="Litologia", font=("Arial", 15)).grid(
                row=2, column=0
            )
            porclab = Label(window, text="Porcentagem", font=("Arial", 15)).grid(
                row=3, column=0
            )
            porclabe = OptionMenu(window, Percvar, *TipV)
            porclabe.grid(row=3, column=1)
            granlab = Label(window, text="Granulometria", font=("Arial", 15)).grid(
                row=4, column=0
            )
            granlabe = OptionMenu(window, Granvar, *TipV)
            granlabe.grid(row=4, column=1)
            global HEAD
            salvar = Button(
                window,
                text="Salvar",
                command=Salvar,
                font=("Comic Sans", 13),
                fg="#DCDCDC",
                bg="black",
                activeforeground="#F8F8FF",
                activebackground="Black",
            )
            salvar.grid(row=5, column=0, columnspan=1, pady=7, padx=7, ipadx=100)
            sair = Button(
                window,
                text="Sair",
                command=SairSalvar,
                font=("Comic Sans", 13),
                fg="#DCDCDC",
                bg="black",
                activeforeground="#F8F8FF",
                activebackground="Black",
            )
            sair.grid(row=5, column=1, columnspan=1, pady=7, padx=7, ipadx=100)
            window.mainloop()

    def SalvarDados():
        window1.destroy()

    window1 = Toplevel(windowmain)
    window1.title("SedBr - Abrir Arquivo")
    window1.resizable(False, False)
    # window1.iconbitmap(r'sedbricon.ico')
    window1.grab_set()
    ent = Entry(window1, font=("Arial", 14), fg="grey", textvariable="Nome do Poço")
    ent.grid(row=0, column=0)
    abr = Button(
        window1,
        text="+",
        command=openFile,
        font=("Comic Sans", 13),
        fg="#DCDCDC",
        bg="black",
        activeforeground="#F8F8FF",
        activebackground="Black",
        width=3,
    )
    abr.grid(row=0, column=1, columnspan=1, pady=7, padx=7, ipadx=100)
    edt = Button(
        window1,
        text="Editar Colunas",
        command=Janela,
        font=("Comic Sans", 13),
        fg="#DCDCDC",
        bg="black",
        activeforeground="#F8F8FF",
        activebackground="Black",
        width=10,
    )
    edt.grid(row=1, column=1, columnspan=1, pady=7, padx=7, ipadx=100)
    salvar = Button(
        window1,
        text="Salvar",
        command=SalvarDados,
        font=("Comic Sans", 13),
        fg="#DCDCDC",
        bg="green",
        activeforeground="#F8F8FF",
        activebackground="Black",
        width=7,
    )
    salvar.grid(row=1, column=0, columnspan=1, pady=7, padx=7, ipadx=100)
    window1.mainloop()


filepath = ""


def openFile():
    global filepath
    filepath = filedialog.askopenfilename(
        initialdir="C:\\Users\\brbru\Desktop\\Programacao\\Tkinter_py",
        title="Open file:",
        filetypes=(
            ("xlsx files", "*.xlsx"),
            ("xls files", "*.xls"),
            ("all files", "*.*"),
        ),
    )
    return filepath


# _______________________________________________________________
def Paletas_Criar():
    windowp = Tk()
    windowp.title("SedBr - Criação de Paletas")
    # windowp.iconbitmap(r'sedbricon.ico')
    windowp.geometry("1000x550")
    windowp.configure(background="#BDB76B")
    backgr = "#98FB98"
    hlbg = "#2F4F4F"
    windowp.resizable(False, False)
    frame = Frame(
        windowp, bd=4, bg=backgr, highlightbackground=hlbg, highlightthickness=3
    )
    # place deixa as janelas autoajustaveis
    frame.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.1)
    frame2 = Frame(
        windowp, bd=4, bg=backgr, highlightbackground=hlbg, highlightthickness=3
    )
    # place deixa as janelas autoajustaveis
    frame2.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.825)

    Mnemonicos = sorted(Dados()[1].unique())  #

    nome_do_dic = "exemplo"

    def Color(pos):
        cor = colorchooser.askcolor()[1]
        if cor:
            cor_botons[pos].config(bg=cor)
            lista_CORES[pos] = cor

    def criar_json_paleta(nome_do_dic, dic_lit):
        with open(nome_do_dic + ".json", "w") as arquivo_json:
            json.dump(dic_lit, arquivo_json)

    def abrindo_dic_lit():
        pass

    def Abrir_paleta_():
        pass

    Tamanho_Mnem = len(Mnemonicos)

    estilo_notebook = ttk.Style()
    estilo_notebook.configure(
        "TNotebook", background=backgr, tabposition="n", highlightbackground=hlbg
    )
    if Tamanho_Mnem <= 39:
        ABA = [frame2]
    else:
        abas = ttk.Notebook(frame2, style="TNotebook")
        aba1 = Frame(abas)
        aba2 = Frame(abas, background=backgr, highlightbackground=hlbg)
        abas.add(aba1, text="Litologias 1")
        aba1.configure(background=backgr, highlightbackground=hlbg)
        aba2.configure(background=backgr)
        abas.add(aba2, text="Litologias 2")
        abas.place(relx=0, rely=0, relwidth=1, relheight=1)
        ABA = [aba1, aba2]
    lista = []
    for i in range(Tamanho_Mnem):
        lista.append(StringVar())
    dic_person_nome = StringVar()
    paletperson = Label(
        frame, text="Nome da Paleta", font=("Arial", 15), bg=backgr
    ).pack(
        side="left", padx=7
    )  # .grid(row=0, column=0,padx=7)
    entdic = Entry(
        frame, textvariable=dic_person_nome, font=("Arial", 14), fg="#4B0082"
    )
    entdic.pack(side="left", padx=7)  # .grid(row=0, column=1,padx=7)
    entdic.insert(0, "paleta_personalizada")

    def Salvar_Paleta():
        # cria e salva a paleta
        if None in lista_CORES:
            answer = messagebox.askyesno(
                title="AVISO -  Litologias sem cor!",
                message="Todas as litologias que estiverem vazias\n serão trocadas pela cor branca.\n\n Deseja continuar mesmo assim? ",
            )
            if answer:
                for i in range(len(lista_CORES)):
                    if lista_CORES[i] == None:
                        lista_CORES[i] = "#ffffff"
            elif answer == False:
                pass
        nome_palet = entdic.get()
        # print("E:",nome_palet)
        # print("COres:",lista_CORES )
        dic_lit = {}
        for c in range(len(Mnemonicos)):
            dic = {
                "short_name": Mnemonicos[c],
                "patch_property": {"color": lista_CORES[c], "hatch": opthatch[c].get()},
            }
            dic_lit[Mnemonicos[c]] = dic
        criar_json_paleta(nome_palet, dic_lit)
        # print(dic_lit)

    cor_botons = []
    lista_CORES = [None] * Tamanho_Mnem
    TipVar = tuple(
        [
            "",
            "/",
            "|",
            "-",
            "+",
            "/-",
            "x",
            ".",
            "..",
            "o",
            "oo",
            "O",
            "-o",
            "+o",
            "xo",
            "-.",
            "-x",
            "-.",
            "-x",
            "-|-",
            "-x-",
            "-o-",
            "-.-",
        ]
    )
    opthatch = [StringVar(frame2) for i in range(Tamanho_Mnem)]
    linh = 10
    colu = round(Tamanho_Mnem // linh)

    def ABAS():
        c = 0
        cl = 0
        ln = ln2 = 0
        ab2 = 4
        if Tamanho_Mnem > 4:
            ln = 4
        if Tamanho_Mnem <= 4:
            ln = Tamanho_Mnem
        if Tamanho_Mnem > 44:
            ln2 = 4
        if Tamanho_Mnem in [41, 42, 43, 44]:
            ln2 = Tamanho_Mnem - 40
        for i in range(10):  # ((colu//4)+1)*10
            for j in range(ln):  # (colu//4)*4+(colu%4)
                # print(i-ln,j-cl)
                if c < Tamanho_Mnem:
                    if i <= 9 and j <= 3:
                        AB = ABA[0]
                        I = i
                        J = 3 * (j)
                        label = Label(
                            AB,
                            text=Mnemonicos[c] + ":",
                            bg=backgr,
                            font=("Comic Sans", 13),
                        )
                        label.grid(row=I + 1, column=J)
                        opthatch[c].set("")
                        opt = OptionMenu(
                            AB, opthatch[c], *TipVar
                        )  # textvariable=lista[c]
                        opt.grid(row=I + 1, column=J + 2)
                        colplus = Button(
                            AB,
                            text="+",
                            font=("Comic Sans", 13),
                            fg="#1C1C1C",
                            bg="#FFFFFF",
                            activeforeground="#000000",
                            activebackground="#FFFFFF",
                            width=5,
                        )
                        colplus.grid(row=I + 1, column=J + 1, padx=7)
                        cor_botons.append(colplus)
                        c += 1
                    else:
                        pass
                else:
                    pass
        if Tamanho_Mnem > 40:
            ab2 = 8
            for i in range(10):
                for j in range(ln2):
                    if c < Tamanho_Mnem:
                        if i <= 9 and j <= 3:
                            AB = ABA[1]
                            I = i
                            J = 3 * (j)
                            label = Label(
                                AB,
                                text=Mnemonicos[c] + ":",
                                bg=backgr,
                                font=("Comic Sans", 13),
                            )
                            label.grid(row=I + 1, column=3 * (j))
                            opthatch[c].set("")
                            opt = OptionMenu(AB, opthatch[c], *TipVar)
                            opt.grid(row=i + 1, column=3 * (j) + 2)
                            colplus = Button(
                                AB,
                                text="+",
                                font=("Comic Sans", 13),
                                fg="#1C1C1C",
                                bg="#FFFFFF",
                                activeforeground="#000000",
                                activebackground="#FFFFFF",
                                width=5,
                            )
                            colplus.grid(row=i + 1, column=3 * (j) + 1, padx=7)
                            cor_botons.append(colplus)
                            c += 1
                    else:
                        pass
        AB = ABA[0]
        cl = 0
        for i in range(ln + ln2):
            if i == 4:
                cl = 4
                AB = ABA[1]
            Corlab = Label(AB, text="Cor", font=("Arial", 14), bg=backgr).grid(
                row=0, column=3 * (i - cl) + 1, padx=7, pady=7
            )
            Litolab = Label(AB, text="Litologia", font=("Arial", 14), bg=backgr).grid(
                row=0, column=3 * (i - cl), padx=7, pady=7
            )
            Hatclab = Label(AB, text="Hatch", font=("Arial", 14), bg=backgr).grid(
                row=0, column=3 * (i - cl) + 2, padx=7, pady=7
            )

    ABAS()
    """if openPalet:
        sv=Button(frame2,text="Abrir", command=Abrir_paleta, font=("Comic Sans",15), fg="#F8F8FF", bg="#2F4F4F", activeforeground="#DCDCDC",activebackground="#5F9EA0", width=10)
        sv.pack(side="left",padx=7)#grid(row=0, column=3,padx=7)"""
    for i in range(len(cor_botons)):
        cb = cor_botons[i]
        cb.config(command=lambda b=i: Color(b))

    sv = Button(
        frame,
        text="Salvar",
        command=Salvar_Paleta,
        font=("Comic Sans", 15),
        fg="#F8F8FF",
        bg="#2F4F4F",
        activeforeground="#DCDCDC",
        activebackground="#5F9EA0",
        width=10,
    )
    sv.pack(side="left", padx=7)  # grid(row=0, column=3,padx=7)
    # sv=Button(frame,text="Abrir", command=Abrir_paleta, font=("Comic Sans",15), fg="#F8F8FF", bg="#2F4F4F", activeforeground="#DCDCDC",activebackground="#5F9EA0", width=10)
    # sv.pack(side="left",padx=7)#grid(row=0, column=3,padx=7)
    windowp.mainloop()


# _______________________________________________________________


def Descricao():
    pass


def Graficos():
    # windowmain.destroy()
    JanelaGrafico()


windowmain = Tk()
windowmain.title("SedBr")
windowmain.resizable(False, False)
# win#dowmain.iconbitmap(r'sedbricon.ico')
abrir = Button(
    windowmain,
    text="Abrir arquivo do Poço",
    command=Abrir,
    font=("Comic Sans", 15),
    fg="#DCDCDC",
    bg="black",
    activeforeground="#F8F8FF",
    activebackground="Black",
)
abrir.grid(row=1, column=1, columnspan=1, pady=7, padx=7, ipadx=100)
descricao = Button(
    windowmain,
    text="Descrição",
    command=Descricao,
    font=("Comic Sans", 15),
    fg="#DCDCDC",
    bg="black",
    activeforeground="#F8F8FF",
    activebackground="Black",
)
descricao.grid(row=2, column=1, columnspan=1, pady=7, padx=7, ipadx=100)
graficos = Button(
    windowmain,
    text="Gráficos",
    command=Graficos,
    font=("Comic Sans", 15),
    fg="#DCDCDC",
    bg="black",
    activeforeground="#F8F8FF",
    activebackground="Black",
)
graficos.grid(row=3, column=1, columnspan=1, pady=7, padx=7, ipadx=100)
windowmain.mainloop()

# pyinstaller --onefile --noconso#le --windowed --icon=sedbricon.ico v003_Sedbr.py
