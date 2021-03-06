# -*- coding: cp936 -*-
import random
from itertools import permutations as perm, combinations as comb
import copy

step = 4
tp = tuple(range(1,10)) 

def gen():
    """生成4位的目标数字"""
    ls = list(tp)
    random.shuffle(ls)
    seed = random.randint(0,step+1)
    return ls[seed:seed+step]

def splitList():
    """将目标list，按步长拆分成几个子lists"""
    return [tp[step*t:step*(t+1)] for t in range(len(tp)/step+(0 if len(tp)%step == 0 else 1))]

def compare(src,target):
    """把候选list和目标list进行比对，返回位置正确和错误数字的个数"""
    e = 0
    w = 0
    if src == target:
        return 4,0
    else:
        for i in src:
            if i in target and src.index(i) == target.index(i):
                e += 1
            elif i in target:
                w += 1
        return e,w

def smash():
    target = gen()
    #print 'target is: %s' % target    
    init = splitList()
    result = {}
    flag = False
    count = 0
    for ls in init[:-1]:             
        x,y = compare(ls,target)
        count += 1
        result[ls] = (x,y)
        if x == step:
            return count #直接在[1,2,3,4]或者[5,6,7,8]中找到了
        elif sum([x+y for x,y in result.values()]) == step:
            flag = True
            break   
    if not flag:
        result[(9,)]=(0,1)
    #首轮判断完毕以后，消除value=(0,0)的子列表
    for x in result.keys():
        e,w = result[x]
        if e + w == 0:
            result.pop(x)
    candy = []
    for i in result:
        candy = merge(candy,guess(i,result[i]))
    #这里断言结果一定在备选列表里，如果不在的话程序肯定猜不出来
    assert(target in [dict2list(c) for c in candy])
    find = False
    while not find:
        tmp = dict2list(candy.pop(0))
        e,w = compare(tmp,target)
        result[tuple(tmp)]=(e,w)
        #print 'result is ', result        
        count += 1
        if e == step:
            find = True
            break
        candy = [c for c in candy if compare(tmp,dict2list(c)) == (e,w)]           
        if e == 0 and w != 0:
            for t in tmp:                
                candy = [c for c in candy
                         if t not in c.keys() or c[t] != tmp.index]
        elif e + w < step:
            candy = [c for c in candy
                     if set(c.keys()) != set(tmp)]
        elif e + w == step:
            candy = [c for c in candy if set(c.keys()) == set(tmp)]
        candy = [c for c in candy if len(set(c.keys()) & set(tmp)) <= e+w]    
    return count
        
def dict2list(adict):
    result = [0,0,0,0]
    for k,v in adict.items():
        result[v] = k
    return result
    
def guess(ls,pattern):    
    m = {i:ls.index(i) for i in ls}
    pl = []
    cl = []
    e,w = pattern        
    if e != 0:
        for p in list(comb(ls,e)):
            ed = {}
            for i in p:                
                ed[i] = m[i]
            pl.append(ed)        
    if w != 0:
        for c in list(comb(ls,w)):
            wd = {}
            for i in c:                               
                wd[i] = range(step)
                #对于位置错误的个数，我们需要将数字原来的位置进行排除
                #但是9除外，因为(9,)没有进行比对，所以不能说9不在第一位
                if i != 9:
                    wd[i].remove(m[i]) 
            cl.extend(unwind(wd))
    return merge(pl,cl)

def unwind(adict):
    """该函数将dict里value为list进行unwind操作
    比如{2:[0,2,3]}解析为[{2:0},{2:2},{2:3}]"""
    result = []
    for k,v in adict.items():
        if result == []:
            result.extend([{k:i} for i in v])
        else:
            for value in v:
                for i in result:
                    if k in i.keys() and value not in i.values():
                        t = copy.deepcopy(i)
                        t[k] = value
                        result.append(t)
                    elif value not in i.values()    :
                        i[k] = value
    return result 
def merge(als,bls):
    """将两个list进行合并，排除元素或者元素位置冲突的组合"""
    result = []
    if als == []:
        result = bls
    elif bls == []:
        result = als
    else:
        for a in als:
            ka = set(a.keys())
            va = set(a.values())
            for b in bls:
                kb = set(b.keys())
                vb = set(b.values())
                if kb&ka == set() and va&vb == set():
                    result.append(dict(a.items()+b.items()))
    return result     

if __name__ == '__main__':
    counter = []
    number = 2000
    for i in range(number):
        counter.append(smash())
    print '%d次里平均猜中所需次数：%f，超过10次的有：%d' % (number,sum(counter)*1.0/number,len([x for x in counter if x >10]))
