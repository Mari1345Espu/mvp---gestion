import React, { useEffect, useState } from 'react';
import convocatoriaService from '../services/convocatoriaService';

function Convocatorias() {
  const [convocatorias, setConvocatorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ 
    nombre: '', 
    fecha_inicio: '', 
    fecha_fin: '', 
    estado: '' 
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchConvocatorias();
  }, []);

  const fetchConvocatorias = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await convocatoriaService.getConvocatorias();
      setConvocatorias(data);
    } catch (error) {
      console.error('Error al cargar convocatorias:', error);
      setError('Error al cargar las convocatorias. Por favor, intente nuevamente.');
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
        await convocatoriaService.updateConvocatoria(editingId, form);
      } else {
        await convocatoriaService.createConvocatoria(form);
      }
      setForm({ nombre: '', fecha_inicio: '', fecha_fin: '', estado: '' });
      setEditingId(null);
      fetchConvocatorias();
    } catch (error) {
      console.error('Error al guardar convocatoria:', error);
      setError('Error al guardar la convocatoria. Por favor, intente nuevamente.');
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
      setError(null);
      try {
        await convocatoriaService.deleteConvocatoria(id);
        fetchConvocatorias();
      } catch (error) {
        console.error('Error al eliminar convocatoria:', error);
        setError('Error al eliminar la convocatoria. Por favor, intente nuevamente.');
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
      <h2 className="mb-4">Gestión de Convocatorias</h2>
      
      {error && (
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          {error}
          <button type="button" className="btn-close" onClick={() => setError(null)}></button>
        </div>
      )}

      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h3 className="card-title h5 mb-3">{editingId ? 'Editar Convocatoria' : 'Crear Nueva Convocatoria'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="row">
              <div className="col-md-6 mb-3">
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
              <div className="col-md-6 mb-3">
                <label className="form-label">Estado</label>
                <select 
                  name="estado" 
                  className="form-select" 
                  value={form.estado} 
                  onChange={handleChange} 
                  required
                >
                  <option value="">Seleccione un estado</option>
                  <option value="activa">Activa</option>
                  <option value="inactiva">Inactiva</option>
                  <option value="finalizada">Finalizada</option>
                </select>
              </div>
            </div>
            <div className="row">
              <div className="col-md-6 mb-3">
                <label className="form-label">Fecha Inicio</label>
                <input 
                  type="date" 
                  name="fecha_inicio" 
                  className="form-control" 
                  value={form.fecha_inicio} 
                  onChange={handleChange} 
                  required 
                />
              </div>
              <div className="col-md-6 mb-3">
                <label className="form-label">Fecha Fin</label>
                <input 
                  type="date" 
                  name="fecha_fin" 
                  className="form-control" 
                  value={form.fecha_fin} 
                  onChange={handleChange} 
                  required 
                />
              </div>
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
                    setForm({ nombre: '', fecha_inicio: '', fecha_fin: '', estado: '' }); 
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
          <h3 className="card-title h5 mb-3">Lista de Convocatorias</h3>
          <div className="table-responsive">
            <table className="table table-hover">
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
                    <td>{new Date(convocatoria.fecha_inicio).toLocaleDateString()}</td>
                    <td>{new Date(convocatoria.fecha_fin).toLocaleDateString()}</td>
                    <td>
                      <span className={`badge bg-${convocatoria.estado === 'activa' ? 'success' : convocatoria.estado === 'inactiva' ? 'warning' : 'secondary'}`}>
                        {convocatoria.estado}
                      </span>
                    </td>
                    <td>
                      <div className="btn-group">
                        <button 
                          className="btn btn-sm btn-outline-primary" 
                          onClick={() => handleEdit(convocatoria)}
                        >
                          <i className="bi bi-pencil"></i>
                        </button>
                        <button 
                          className="btn btn-sm btn-outline-danger" 
                          onClick={() => handleDelete(convocatoria.id)}
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

export default Convocatorias;
