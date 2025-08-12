# 定义 RSA 模块
module RSA
  require "prime"
  require "openssl"

  def self.generate_keys
    puts "开始生成 RSA 密钥对 ..."

    # 生成两个大素数 p 和 q
    p = generate_prime(1536)
    q = generate_prime(1536)

    puts "产生随机质数（1536 位）："
    puts "p: #{p}"
    puts "q: #{q}"

    # 确保 p 和 q 不相等
    while p == q
      q = generate_prime(1536)
    end

    n = p * q
    puts "计算模数 n = p * q（3072 位）: #{n}"

    phi_n = (p - 1) * (q - 1)
    puts "计算欧拉函数 phi = (p - 1) * (q - 1): #{phi_n}"

    e = 65537
    puts "选择公钥指数 e = #{e}"

    # 计算私钥指数 d，使用 OpenSSL::BN 大数来计算模逆元
    d = OpenSSL::BN.new(e.to_s).mod_inverse(phi_n)
    puts "计算私钥指数 d = #{d}"

    public_key = { n: n, e: e }
    private_key = { p: p, q: q, n: n, d: d }

    # 返回公钥和私钥
    { public_key: public_key, private_key: private_key }
  end

  # 添加生成指定位数素数的方法
  def self.generate_prime(bits)
    while true
      # 生成随机的 bits 位数字
      candidate = OpenSSL::BN.rand(bits, -1, true)
      # 确保是素数
      return candidate if candidate.prime?
    end
  end

  # 加密方法
  def self.encrypt(message, public_key)
    message.chars.map do |char|
      encrypted = OpenSSL::BN.new(char.ord.to_s).mod_exp(public_key[:e], public_key[:n]) # 使用公钥加密每个字符
      encrypted.to_i.to_s
    end
  end

  # 解密方法
  def self.decrypt(encrypted_message, private_key)
    encrypted_message.map do |char|
      decrypted = OpenSSL::BN.new(char.to_s).mod_exp(private_key[:d], private_key[:n]) # 使用私钥解密每个字符
      decrypted.to_i.chr
    end.join
  end
end

# 混合模块到类中
class RSAApp
  include RSA # 混合 RSA 模块

  attr_reader :keys

  def initialize
    @keys = RSA.generate_keys
    display_keys # 添加显示密钥的调用
  end

  def display_keys
    puts "\n=== RSA 密钥对 ==="
    puts "公钥 (Public Key):"
    puts "  n: #{@keys[:public_key][:n]}"
    puts "  e: #{@keys[:public_key][:e]}"
    puts "\n私钥 (Private Key):"
    puts "  p: #{@keys[:private_key][:p]}"
    puts "  q: #{@keys[:private_key][:q]}"
    puts "  n: #{@keys[:private_key][:n]}"
    puts "  d: #{@keys[:private_key][:d]}"
    puts "==================\n\n"
  end

  def encrypt_message(message)
    puts "\n=== 加密消息 ==="
    puts "  原始消息：#{message}"
    encrypted = RSA.encrypt(message, keys[:public_key])
    puts "  加密消息：#{encrypted.inspect}"
    puts "==================\n\n"
    encrypted
  end

  def decrypt_message(encrypted)
    puts "\n=== 解密消息 ==="
    puts "  加密消息：#{encrypted.inspect}"
    message = RSA.decrypt(encrypted, keys[:private_key])
    puts "  解密消息：#{message}"
    puts "==================\n\n"
    message
  end
end

# 测试类
class RSATester
  def self.run
    app = RSAApp.new

    # 用户输入待加密消息
    puts "请输入一段消息进行 RSA 加密："
    message = gets.chomp

    # 加密过程
    encrypted_message = app.encrypt_message(message)

    # 解密过程
    decrypted_message = app.decrypt_message(encrypted_message)
  end
end

# 启动测试
RSATester.run
