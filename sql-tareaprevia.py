empleado_01=[[20222333,45,2,20000],
             [33456234,40,0,25000],
             [45432345,41,1,10000]]
             
def superanSalarioBloque01(empleados):
    res = []
    for f in empleados:
        if(f[3]>15000):
            res.append(f)
    return res             
    
supSalBloque01 = superanSalarioBloque01(empleado_01)

for f in supSalBloque01:
    print(f)
    
empleado_02=[[20222333,45,2,20000],
             [33456234,40,0,25000],
             [45432345,41,1,10000],
             [43967304,37,0,12000],
             [42236276,36,0,18000]]
             
             
empleado_03=[[20222333,20000,45,2],
             [33456234,25000,40,0],
             [45432345,10000,41,1],
             [43967304,12000,37,0],
             [42236276,18000,36,0]]
             
             
def superanSalarioBloque03(empleados):
    copia = empleados.copy()
    res = []
    for f in copia:
        if(f[1]>15000):
            f[1], f[2] = f[2], f[1]
            f[2], f[3] = f[3], f[2]
            res.append(f)
    return res  
    
    
    
    
print(superanSalarioBloque03(empleado_03))



empleado_04=[[20222333,33456234,45432345,43967304,42236276],
             [20000,25000,10000,12000,18000],
             [45,40,41,37,36],
             [2,0,1,0,0]]
             
             
def superanSalarioBloque04(empleados):
    copia = empleados.copy()
    res = []
    for n in range(len(copia[0])):
        if(copia[1][n]>15000):
            res.append([copia[0][n],copia[3][n],copia[2][n],copia[1][n]])
    return res             
    
    
print(superanSalarioBloque04(empleado_04))    

    
