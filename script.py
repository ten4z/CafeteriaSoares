# coding = utf-8
import bge
cont = bge.logic.getCurrentController()
own = cont.owner
scn = own.scene
scl = bge.logic.getSceneList()
obj = scn.objects
# -> DATABASE <- #
# Commit quando INSERIR ou ATUALIZAR
import sqlite3
class dbSetup():
    #db = bge.logic.expandPath("\\")
    conexao = sqlite3.connect("001d.db")
    cursor = conexao.cursor()
    def criarTabela(self):        
        sql = """ CREATE TABLE IF NOT EXISTS tb_produtos( id_prodt INTEGER PRIMARY KEY AUTOINCREMENT, nome_prodt TEXT (25) NOT NULL, tipo_prodt TEXT (25), preco_prodt DECIMAL (10,2))"""
        self.cursor.execute(sql)
        # -> VERIFICAR SE EXISTE DADOS <- #
        self.cursor.execute("SELECT * FROM tb_produtos")
        self.data = self.cursor.fetchall()        
        if len(self.data) == 0:
            self.inserirProdutos()        
    def inserirProdutos(self):        
        # -> INSERIR DADOS <- #
        produtos = [['1','café','bebida','4.50'],['2','água','bebida', '3.0'],['3','chá','bebida', '3.5'],
                      ['4','leite','bebida', '5.0'],['5','refrigerante','bebida','7.0'],
                      ['6','pão com manteiga','comida','2.50'],['7','brigadeiro','comida','3.0'],
                      ['8','bolo','comida','2.5'],['9','chimango','comida','5.0'],['10','pão de queijo','comida', '4.0']]     
        for prod in produtos:
            self.cursor.execute("""INSERT INTO tb_produtos (id_prodt, nome_prodt, tipo_prodt, preco_prodt) VALUES (?,?,?,?)""",(prod),)
            self.conexao.commit()
    def selecionarProdutos(self, txt):
        self.cursor.execute("SELECT * FROM tb_produtos")
        self.conexao.commit()
        data = self.cursor.fetchall()        
        for dt in range(0, len(data)):
            self.verificar(data[dt]) 
    def inserirProduto(self, nome, tipo, preco):
        ver_sql = "SELECT nome_prodt FROM tb_produtos WHERE nome_prodt = ?"
        self.cursor.execute(ver_sql, (nome,),)   
        data = self.cursor.fetchone()
        sql = "INSERT INTO tb_produtos (nome_prodt, tipo_prodt, preco_prodt) VALUES (?,?,?)"       
        #print(data)
        if data is None:
            #if cont.sensors['tap'].positive:
            self.cursor.execute(sql, (nome, tipo, preco),)
            self.conexao.commit()
            obj['txt_debug']['Text'] = ""
    def atualizarProduto(self, id, nome, tipo, preco):
        id_sql = "SELECT id_prodt FROM tb_produtos WHERE nome_prodt = ?"
        upd_sql = "UPDATE tb_produtos SET (nome_prodt = ?, tipo_prodt = ?, preco_prodt= ?) WHERE (id_prod = ?)" 
        self.cursor.execute(id_sql, (id,),) 
        data = self.cursor.fetchone()
        if data is None:
            obj['txt_status']['Text'] = "linha não encontrada." 
        else:
            id = data[0]
            self.cursor.execute(upd_sql, (id, nome, tipo, preco),) 
            obj['txt_status']['Text'] = "linha removida." 
            obj['txt_comando']['Text'] = "$ "
    def removerProduto(self, id):
        sel_sql = "SELECT nome_prodt FROM tb_produtos WHERE id_prodt = ?"
        del_sql = "DELETE FROM tb_produtos WHERE id_prodt = ?"        
        self.cursor.execute(sel_sql, (id,),) 
        data = self.cursor.fetchone()
        if data is None:
            obj['txt_status']['Text'] = "linha não encontrada." 
        else:
            self.cursor.execute(del_sql, (id,),) 
            obj['txt_status']['Text'] = "linha removida." 
            obj['txt_comando']['Text'] = "$ "

    def verificar(self, texto):
        txt = obj['txt_comando']['Text']
        txt = txt.replace('$ ', '')
        
        if len(txt) >= 3 and texto != "apagar":
            if txt in str(texto):
                if str(texto) not in obj['txt_debug']['Text']:                
                    obj['txt_debug']['Text'] += str(texto) + '\n'                  
                else:
                    if cont.sensors['tap'].positive:
                        obj['txt_debug']['Text'] = ''
    def lerComando(self, cmd): 
        num = 0
        if cmd == "$ clear" or cmd == "$ limpar":
            obj['txt_debug']['Text'] = ''        
        lista_cmd  = []
        if cmd == '' or cmd == '$':
            obj['txt_comando']['Text']= "$ "
        if 'remove' in cmd and "go" in cmd: 
            print("remover")           
            num = cmd.count(',')           
            if num == 2:
                lista_cmd = cmd.split(',')  
                self.removerProduto(lista_cmd[1])
                print("remover por id")
                obj['txt_status']['Text'] = 'linha removida'
        if 'atualize' in cmd and "go" in cmd: 
            print("atualizar")           
            num = cmd.count(',')           
            if num == 5:
                lista_cmd = cmd.split(',')  
                self.atualizarProduto(lista_cmd[1], lista_cmd[2], lista_cmd[3])
                print("atualizar por id")  
                obj['txt_status']['Text'] = 'linha atualizada'       
        if 'insere' in cmd and "go" in cmd: 
            num = cmd.count(',')           
            if num == 4: 
                lista_cmd = cmd.split(',')     
                self.inserirProduto(lista_cmd[1], lista_cmd[2], lista_cmd[3]) 
                obj['txt_status']['Text'] = 'linha inserida.'
class Game():
    def iniciar(self):
        print("Game iniciado.")
        obj['txt_main'].resolution = 5
        obj['txt_debug'].resolution = 5
        obj['txt_comando'].resolution = 5
        obj['txt_status'].resolution = 5
        cont.activate(cont.actuators['back_scene'])
    def atualizar(self):
        #print("Game executando...")
        dbSetup().selecionarProdutos(obj['txt_comando']['Text'])
        dbSetup().lerComando(obj['txt_comando']['Text'])
def run():
    g = Game()
    if cont.sensors['iniciar'].positive:
        g.iniciar()
        dbSetup().criarTabela()
    if cont.sensors['atualizar'].positive:
        g.atualizar()            
if __name__ == "__main__":
    Game().atualizar()