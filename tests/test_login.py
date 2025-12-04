from controllers.auth_controller import auth

print("🔍 Testando login...")
resultado = auth.login("admin@sisusf.com", "admin123", "127.0.0.1")

# Imprime só o que importa
print(f"\n✅ Success: {resultado['success']}")
print(f"📧 Message: {resultado['message']}")

if resultado['success']:
    print(f"👤 Usuário logado: {resultado['user'].nome}")
    print("\n🎉🎉🎉 LOGIN FUNCIONOU!!!! 🎉🎉🎉")
else:
    print("\n❌ Falhou")

# Testa outras senhas
print("\n" + "="*50)
print("Testando outras combinações:")
senhas_teste = ["admin123", "Admin123", "medico123"]
for senha in senhas_teste:
    resultado = auth.login("admin@sisusf.com", senha, "127.0.0.1")
    status = "✅" if resultado['success'] else "❌"
    print(f"{status} Senha '{senha}': {resultado['success']}")