import utils.tools as tools
js = '''
    function(e, t) {
        var t = {}
        var i = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz".split("");
        e = e || 10;
        for (var n = "", o = 0; o < e; o++)
            n += i[Math.floor(Math.random() * i.length)];
        return n + (t ? Date.now().toString(32) : "")
    }
'''

a = tools.exec_js(js)
print(a)


