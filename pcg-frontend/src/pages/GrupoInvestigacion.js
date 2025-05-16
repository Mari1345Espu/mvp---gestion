import React, { useEffect, useState } from 'react';
import grupoService from '../services/grupoinvestigacionService';

function GrupoInvestigacion() {
  const [grupos, setGrupos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ nombre: '', descripcion: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchGrupos();
  }, []);

  const fetchGrupos = async () => {
    setLoading(true);
    try {
      const data = await grupoService.getGrupos();
      setGrupos(data);
    } catch (error) {
      alert('Error al cargar grupos de investigación');
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
        await grupoService.updateGrupo(editingId, form);
      } else {
        await grupoService.createGrupo(form);
      }
      setForm({ nombre: '', descripcion: '' });
      setEditingId(null);
      fetchGrupos();
    } catch (error) {
      alert('Error al guardar grupo de investigación');
    }
  };

  const handleEdit = (grupo) => {
    setForm({
      nombre: grupo.nombre,
      descripcion: grupo.descripcion || ''
    });
    setEditingId(grupo.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este grupo de investigación?')) {
      try {
        await grupoService.deleteGrupo(id);
        fetchGrupos();
      } catch (error) {
        alert('Error al eliminar grupo de investigación');
      }
    }
  };

  return (
    <div>
      <h2>Grupos de Investigación</h2>
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
            {grupos.map(grupo => (
              <tr key={grupo.id}>
                <td>{grupo.nombre}</td>
                <td>{grupo.descripcion}</td>
                <td>
                  <button className="btn btn-sm btn-primary me-2" onClick={() => handleEdit(grupo)}>Editar</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(grupo.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>{editingId ? 'Editar Grupo de Investigación' : 'Crear Grupo de Investigación'}</h3>
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

export default GrupoInvestigacion;
