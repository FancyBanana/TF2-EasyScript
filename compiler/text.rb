def stitch_files(file_list, destination)
    fout = File.new(destination, 'w+')
    file_list.each{|file|
        fin = File.new(file, 'r+')
        fin.each{|line| fout << line}
        fout << "\n"
    }
end

def prep_line(tmp)
    return nil unless tmp = /^[^#]+/.match(tmp)
    return nil unless /\S+/.match(tmp[0])
    tmp = tmp[0].split(/[\|\:]/);
    tmp = tmp.map{|line|
        /\S+/.match(line) ? /^\s*(\S.*?)\s*$/.match(line)[1] : nil
    }
    return tmp;
end;

def array_subst(src, dest)
    src.each_with_index{|o,i| dest[i] = o;}
    return dest
end;

def r_sign(text)
    if text =~ /\+/ then
        return text.gsub(/\+/,'-')
    elsif text =~ /\-/ then
        return text.gsub(/\-/,'+')
    else
        return nil
    end
end

def m_alias(var)
if String === var then
    return r_sign(var)
elsif Array === var then
    var2 = []
    var.each{|com| var2 << r_sign(com)}
    return var2.compact
end
end

def read_group(filehandle)
    res = Array.new
    names = [:name, :funct, :bind, :secondary, :next, :prev]
    filehandle.each do |line|
        l = Array.new(6)
        p = prep_line(line);
        next unless p;
        array_subst(p,l)
        h = Hash.new
        l.each_with_index{|o,i|
            h[names[i]] = o
        }
        res << h
    end
    return res
end

def read_options(filehandle)
    opts = {modifiers: 'no', callback: 'no',qswitch: 'no', lastinv: nil, invnext: nil, invprev: nil}
    filehandle.each do |line|
        p = prep_line(line);
        next unless p
        case p[0]
        when /modifiers/i then
            opts[:modifiers] = p[1]
        when /callback/i then
            opts[:callback] = p[1]
        when /qswitch/i then
            opts[:qswitch] = p[1]
        when /lastinv/i then
            opts[:lastinv] = p[1]
        when /invnext/i then
            opts[:invnext] = p[1]
        when /invprev/i then
            opts[:invprev] = p[1]
        end
    end
    return opts
end

def read_modifiers(filehandle)
    res = Array.new
    names = [:name, :type]
    filehandle.each do |line|
        l = Array.new(2,nil)
        p = prep_line(line);
        next unless p;
        array_subst(p,l)
        h = Hash.new
        l.each_with_index{|o,i|
            h[names[i]] = o
        }
        res << h
    end
    return res
end