import React, { useEffect, useState } from 'react';
import usuarioService from '../services/usuarioService';
import rolService from '../services/rolService';
import grupoService from '../services/grupoinvestigacionService';

function Dashboard() {
  const [usuariosCount, setUsuariosCount] = useState(0);
  const [rolesCount, setRolesCount] = useState(0);
  const [gruposCount, setGruposCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCounts() {
      setLoading(true);
      try {
        const usuarios = await usuarioService.getUsuarios();
        const roles = await rolService.getRoles();
        const grupos = await grupoService.getGrupos();
        setUsuariosCount(usuarios.length);
        setRolesCount(roles.length);
        setGruposCount(grupos.length);
      } catch (error) {
        console.error('Error fetching counts', error);
      }
      setLoading(false);
    }
    fetchCounts();
  }, []);

  if (loading) {
    return <p>Cargando dashboard...</p>;
  }

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="row">
        <div className="col-md-4">
          <div className="card text-white bg-primary mb-3">
            <div className="card-header">Usuarios</div>
            <div className="card-body">
              <h5 className="card-title">{usuariosCount}</h5>
              <p className="card-text">Total de usuarios registrados</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-white bg-success mb-3">
            <div className="card-header">Roles</div>
            <div className="card-body">
              <h5 className="card-title">{rolesCount}</h5>
              <p className="card-text">Total de roles definidos</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-white bg-info mb-3">
            <div className="card-header">Grupos de Investigación</div>
            <div className="card-body">
              <h5 className="card-title">{gruposCount}</h5>
              <p className="card-text">Total de grupos de investigación</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
