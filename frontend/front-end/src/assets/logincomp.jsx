import React, { useEffect, useState } from "react";


export default function Login(){
    const [nome, setNome] = useState ("")
    const [senha, setSenha] = useState("")
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();


const logar = async (e) => {
    e.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      // 1) Login e pega o token JWT
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        nome: nome,
        senha: senha,
      });

      const access = response.data.access;
      console.log("XXX", access);
      
      // Salva o token
      localStorage.setItem("token", access);

      // 2) Busca os dados do usuário logado
      const me = await axios.get("http://127.0.0.1:8000/api/usuarios/me/", {
        headers: { Authorization: `Bearer ${access}` },
      });
      
      const { is_superuser, is_staff, is_active } = me.data;

      
      // 3) Se usuário estiver inativo, bloqueia
      if (!is_active) {
        localStorage.removeItem("token");
        setMessage("Usuário inativo. Contate o administrador.");
        setLoading(false);
        return;
      }

      // 4) Redirecionamento por perfil
      if (is_staff) {
        navigate("/admin/home");
      } else {
        navigate("/operador/home");
      }
    } catch (error) {
      console.log("Error: ", error);
      localStorage.removeItem("token");
      setMessage("Usuário ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  };

    return(
        <div className="loginPage">
      <div className="loginCard">
        <div className="loginHeader">
          <h1 className="loginTitle">Acessar sistema</h1>
          <p className="loginSubtitle">Entre com suas credenciais para continuar</p>
        </div>

        <form className="loginForm" onSubmit={logar}>
          <div className="field">
            <label className="label">Usuário</label>
            <input
              className="input"
              value={nome}
              onChange={(e) => setUser(e.target.value)}
              placeholder="Digite seu usuário"
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label className="label">Senha</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Digite sua senha"
              autoComplete="current-password"
            />
          </div>

          {message && <div className="alert">{message}</div>}

          <button className="btnPrimary" type="submit" disabled={loading}>
            {loading ? "Entrando..." : "Entrar"}
          </button>

          <div className="divider">
            <span>ou</span>
          </div>

          <div className="footerActions">
            <p className="footerText">
              Ainda não tem conta?{" "}
              <Link className="link" to="/register">
                Cadastre-se
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
    )
}