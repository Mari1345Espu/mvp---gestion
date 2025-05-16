import React, { useEffect, useState } from 'react';
import rolService from '../services/rolService';

function Roles() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ nombre: '', descripcion: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    setLoading(true);
    try {
      const data = await rolService.getRoles();
      setRoles(data);
    } catch (error) {
      alert('Error al cargar roles');
    }
    setLoading(false);
  };

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
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
      alert('Error al guardar rol');
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
      try {
        await rolService.deleteRol(id);
        fetchRoles();
      } catch (error) {
        alert('Error al eliminar rol');
      }
    }
  };

  return (
    <div>
      <h2>Roles</h2>
      {loading ? <p>Cargando...</p> : (
        <table className="table table-striped">
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
                  <button className="btn btn-sm btn-primary me-2" onClick={() => handleEdit(rol)}>Editar</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(rol.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>{editingId ? 'Editar Rol' : 'Crear Rol'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Nombre</label>
          <input type="text" name="nombre" className="form-control" value={form.nombre} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Descripción</label>
          <textarea name="descripcion" className="form-control" value={form.descripcion} onChange={handleChange} />
        </div>
        <button type="submit" className="btn btn-success">{editingId ? 'Actualizar' : 'Crear'}</button>
        {editingId && <button type="button" className="btn btn-secondary ms-2" onClick={() => { setForm({ nombre: '', descripcion: '' }); setEditingId(null); }}>Cancelar</button>}
      </form>
    </div>
  );
}

export default Roles;
