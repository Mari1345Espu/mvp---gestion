import React, { useEffect, useState } from 'react';
import estadoService from '../services/estadoService';

function Estados() {
  const [estados, setEstados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ nombre: '', tipo_entidad: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchEstados();
  }, []);

  const fetchEstados = async () => {
    setLoading(true);
    try {
      const data = await estadoService.getEstados();
      setEstados(data);
    } catch (error) {
      alert('Error al cargar estados');
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
        await estadoService.updateEstado(editingId, form);
      } else {
        await estadoService.createEstado(form);
      }
      setForm({ nombre: '', tipo_entidad: '' });
      setEditingId(null);
      fetchEstados();
    } catch (error) {
      alert('Error al guardar estado');
    }
  };

  const handleEdit = (estado) => {
    setForm({
      nombre: estado.nombre,
      tipo_entidad: estado.tipo_entidad || ''
    });
    setEditingId(estado.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este estado?')) {
      try {
        await estadoService.deleteEstado(id);
        fetchEstados();
      } catch (error) {
        alert('Error al eliminar estado');
      }
    }
  };

  return (
    <div>
      <h2>Estados</h2>
      {loading ? <p>Cargando...</p> : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo de Entidad</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {estados.map(estado => (
              <tr key={estado.id}>
                <td>{estado.nombre}</td>
                <td>{estado.tipo_entidad}</td>
                <td>
                  <button className="btn btn-sm btn-primary me-2" onClick={() => handleEdit(estado)}>Editar</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(estado.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>{editingId ? 'Editar Estado' : 'Crear Estado'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Nombre</label>
          <input type="text" name="nombre" className="form-control" value={form.nombre} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Tipo de Entidad (opcional)</label>
          <input type="text" name="tipo_entidad" className="form-control" value={form.tipo_entidad} onChange={handleChange} />
        </div>
        <button type="submit" className="btn btn-success">{editingId ? 'Actualizar' : 'Crear'}</button>
        {editingId && <button type="button" className="btn btn-secondary ms-2" onClick={() => { setForm({ nombre: '', tipo_entidad: '' }); setEditingId(null); }}>Cancelar</button>}
      </form>
    </div>
  );
}

export default Estados;
