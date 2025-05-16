import React, { useEffect, useState } from 'react';
import permisoService from '../services/permisoService';

function Permisos() {
  const [permisos, setPermisos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ nombre: '', descripcion: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchPermisos();
  }, []);

  const fetchPermisos = async () => {
    setLoading(true);
    try {
      const data = await permisoService.getPermisos();
      setPermisos(data);
    } catch (error) {
      alert('Error al cargar permisos');
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
        await permisoService.updatePermiso(editingId, form);
      } else {
        await permisoService.createPermiso(form);
      }
      setForm({ nombre: '', descripcion: '' });
      setEditingId(null);
      fetchPermisos();
    } catch (error) {
      alert('Error al guardar permiso');
    }
  };

  const handleEdit = (permiso) => {
    setForm({
      nombre: permiso.nombre,
      descripcion: permiso.descripcion || ''
    });
    setEditingId(permiso.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este permiso?')) {
      try {
        await permisoService.deletePermiso(id);
        fetchPermisos();
      } catch (error) {
        alert('Error al eliminar permiso');
      }
    }
  };

  return (
    <div>
      <h2>Permisos</h2>
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
            {permisos.map(permiso => (
              <tr key={permiso.id}>
                <td>{permiso.nombre}</td>
                <td>{permiso.descripcion}</td>
                <td>
                  <button className="btn btn-sm btn-primary me-2" onClick={() => handleEdit(permiso)}>Editar</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(permiso.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>{editingId ? 'Editar Permiso' : 'Crear Permiso'}</h3>
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

export default Permisos;
