import React, { useEffect, useState } from 'react';
import convocatoriaService from '../services/convocatoriaService';

function Convocatorias() {
  const [convocatorias, setConvocatorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ nombre: '', fecha_inicio: '', fecha_fin: '', estado: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchConvocatorias();
  }, []);

  const fetchConvocatorias = async () => {
    setLoading(true);
    try {
      const data = await convocatoriaService.getConvocatorias();
      setConvocatorias(data);
    } catch (error) {
      alert('Error al cargar convocatorias');
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
        await convocatoriaService.updateConvocatoria(editingId, form);
      } else {
        await convocatoriaService.createConvocatoria(form);
      }
      setForm({ nombre: '', fecha_inicio: '', fecha_fin: '', estado: '' });
      setEditingId(null);
      fetchConvocatorias();
    } catch (error) {
      alert('Error al guardar convocatoria');
    }
  };

  const handleEdit = (convocatoria) => {
    setForm({
      nombre: convocatoria.nombre,
      fecha_inicio: convocatoria.fecha_inicio,
      fecha_fin: convocatoria.fecha_fin,
      estado: convocatoria.estado
    });
    setEditingId(convocatoria.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar esta convocatoria?')) {
      try {
        await convocatoriaService.deleteConvocatoria(id);
        fetchConvocatorias();
      } catch (error) {
        alert('Error al eliminar convocatoria');
      }
    }
  };

  return (
    <div>
      <h2>Convocatorias</h2>
      {loading ? <p>Cargando...</p> : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Fecha Inicio</th>
              <th>Fecha Fin</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {convocatorias.map(convocatoria => (
              <tr key={convocatoria.id}>
                <td>{convocatoria.nombre}</td>
                <td>{convocatoria.fecha_inicio}</td>
                <td>{convocatoria.fecha_fin}</td>
                <td>{convocatoria.estado}</td>
                <td>
                  <button className="btn btn-sm btn-primary me-2" onClick={() => handleEdit(convocatoria)}>Editar</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(convocatoria.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>{editingId ? 'Editar Convocatoria' : 'Crear Convocatoria'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Nombre</label>
          <input type="text" name="nombre" className="form-control" value={form.nombre} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Fecha Inicio</label>
          <input type="date" name="fecha_inicio" className="form-control" value={form.fecha_inicio} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Fecha Fin</label>
          <input type="date" name="fecha_fin" className="form-control" value={form.fecha_fin} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Estado</label>
          <select name="estado" className="form-select" value={form.estado} onChange={handleChange} required>
            <option value="">Seleccione</option>
            <option value="activa">Activa</option>
            <option value="inactiva">Inactiva</option>
          </select>
        </div>
        <button type="submit" className="btn btn-success">{editingId ? 'Actualizar' : 'Crear'}</button>
        {editingId && <button type="button" className="btn btn-secondary ms-2" onClick={() => { setForm({ nombre: '', fecha_inicio: '', fecha_fin: '', estado: '' }); setEditingId(null); }}>Cancelar</button>}
      </form>
    </div>
  );
}

export default Convocatorias;
