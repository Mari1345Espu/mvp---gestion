import React, { useEffect, useState } from 'react';
import rolService from '../services/rolService';

function Roles() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ nombre: '', descripcion: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await rolService.getRoles();
      setRoles(data);
    } catch (error) {
      console.error('Error al cargar roles:', error);
      setError('Error al cargar los roles. Por favor, intente nuevamente.');
    }
    setLoading(false);
  };

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (editingId) {
        await rolService.updateRol(editingId, form);
      } else {
        await rolService.createRol(form);
      }
      setForm({ nombre: '', descripcion: '' });
      setEditingId(null);
      fetchRoles();
    } catch (error) {
      console.error('Error al guardar rol:', error);
      setError('Error al guardar el rol. Por favor, intente nuevamente.');
    }
  };

  const handleEdit = (rol) => {
    setForm({
      nombre: rol.nombre,
      descripcion: rol.descripcion || ''
    });
    setEditingId(rol.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este rol?')) {
      setError(null);
      try {
        await rolService.deleteRol(id);
        fetchRoles();
      } catch (error) {
        console.error('Error al eliminar rol:', error);
        setError('Error al eliminar el rol. Por favor, intente nuevamente.');
      }
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{height: '60vh'}}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-4">Gestión de Roles</h2>
      
      {error && (
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          {error}
          <button type="button" className="btn-close" onClick={() => setError(null)}></button>
        </div>
      )}

      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h3 className="card-title h5 mb-3">{editingId ? 'Editar Rol' : 'Crear Nuevo Rol'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Nombre</label>
              <input 
                type="text" 
                name="nombre" 
                className="form-control" 
                value={form.nombre} 
                onChange={handleChange} 
                required 
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Descripción</label>
              <textarea 
                name="descripcion" 
                className="form-control" 
                value={form.descripcion} 
                onChange={handleChange}
                rows="3"
              />
            </div>
            <div className="d-flex gap-2">
              <button type="submit" className="btn btn-success">
                {editingId ? 'Actualizar' : 'Crear'}
              </button>
              {editingId && (
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={() => { 
                    setForm({ nombre: '', descripcion: '' }); 
                    setEditingId(null); 
                  }}
                >
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </div>
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <h3 className="card-title h5 mb-3">Lista de Roles</h3>
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Descripción</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {roles.map(rol => (
                  <tr key={rol.id}>
                    <td>{rol.nombre}</td>
                    <td>{rol.descripcion}</td>
                    <td>
                      <div className="btn-group">
                        <button 
                          className="btn btn-sm btn-outline-primary" 
                          onClick={() => handleEdit(rol)}
                        >
                          <i className="bi bi-pencil"></i>
                        </button>
                        <button 
                          className="btn btn-sm btn-outline-danger" 
                          onClick={() => handleDelete(rol.id)}
                        >
                          <i className="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Roles;
