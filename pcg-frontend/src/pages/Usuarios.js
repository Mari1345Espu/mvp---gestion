import React, { useEffect, useState } from 'react';
import usuarioService from '../services/usuarioService';

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ correo: '', nombre: '', contraseña: '', telefono: '', foto: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const fetchUsuarios = async () => {
    setLoading(true);
    try {
      const data = await usuarioService.getUsuarios();
      setUsuarios(data);
    } catch (error) {
      alert('Error al cargar usuarios');
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
        await usuarioService.updateUsuario(editingId, form);
      } else {
        await usuarioService.createUsuario(form);
      }
      setForm({ correo: '', nombre: '', contraseña: '', telefono: '', foto: '' });
      setEditingId(null);
      fetchUsuarios();
    } catch (error) {
      alert('Error al guardar usuario');
    }
  };

  const handleEdit = (usuario) => {
    setForm({
      correo: usuario.correo,
      nombre: usuario.nombre,
      contraseña: usuario.contraseña,
      telefono: usuario.telefono,
      foto: usuario.foto
    });
    setEditingId(usuario.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este usuario?')) {
      try {
        await usuarioService.deleteUsuario(id);
        fetchUsuarios();
      } catch (error) {
        alert('Error al eliminar usuario');
      }
    }
  };

  return (
    <div>
      <h2>Usuarios</h2>
      {loading ? <p>Cargando...</p> : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Correo</th>
              <th>Nombre</th>
              <th>Contraseña</th>
              <th>Teléfono</th>
              <th>Foto</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map(usuario => (
              <tr key={usuario.id}>
                <td>{usuario.correo}</td>
                <td>{usuario.nombre}</td>
                <td>{usuario.contraseña}</td>
                <td>{usuario.telefono}</td>
                <td>{usuario.foto}</td>
                <td>
                  <button className="btn btn-sm btn-primary me-2" onClick={() => handleEdit(usuario)}>Editar</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(usuario.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>{editingId ? 'Editar Usuario' : 'Crear Usuario'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Correo</label>
          <input type="email" name="correo" className="form-control" value={form.correo} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Nombre</label>
          <input type="text" name="nombre" className="form-control" value={form.nombre} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Contraseña</label>
          <input type="password" name="contraseña" className="form-control" value={form.contraseña} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Teléfono</label>
          <input type="text" name="telefono" className="form-control" value={form.telefono} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label>Foto</label>
          <input type="text" name="foto" className="form-control" value={form.foto} onChange={handleChange} />
        </div>
        <button type="submit" className="btn btn-success">{editingId ? 'Actualizar' : 'Crear'}</button>
        {editingId && <button type="button" className="btn btn-secondary ms-2" onClick={() => { setForm({ correo: '', nombre: '', contraseña: '', telefono: '', foto: '' }); setEditingId(null); }}>Cancelar</button>}
      </form>
    </div>
  );
}

export default Usuarios;
