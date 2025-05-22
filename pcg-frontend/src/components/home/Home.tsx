import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  Chip,
  Stack,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { proyectoService } from '../../services/proyectoService';
import { programaService } from '../../services/programaService';
import { Proyecto, Programa } from '../../types';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [programas, setProgramas] = useState<Programa[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEstado, setSelectedEstado] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [proyectosData, programasData] = await Promise.all([
          proyectoService.getProyectos(),
          programaService.getProgramas()
        ]);
        setProyectos(proyectosData.content);
        setProgramas(programasData);
      } catch (error) {
        console.error('Error al cargar datos:', error);
      }
    };

    fetchData();
  }, []);

  const filteredProyectos = proyectos.filter((proyecto) => {
    const matchesSearch = proyecto.nombre
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesEstado = !selectedEstado || proyecto.estado === selectedEstado;
    return matchesSearch && matchesEstado;
  });

  const estados = Array.from(new Set(proyectos.map((p) => p.estado)));

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Bienvenido a la Plataforma de Gestión
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Explora nuestros programas y proyectos activos
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ mb: 2 }}>
                <TextField
                  fullWidth
                  label="Buscar proyectos"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip
                    label="Todos"
                    onClick={() => setSelectedEstado('')}
                    color={selectedEstado === '' ? 'primary' : 'default'}
                  />
                  {estados.map((estado) => (
                    <Chip
                      key={estado}
                      label={estado}
                      onClick={() => setSelectedEstado(estado)}
                      color={selectedEstado === estado ? 'primary' : 'default'}
                    />
                  ))}
                </Stack>
              </Box>

              <Grid container spacing={2}>
                {filteredProyectos.map((proyecto) => (
                  <Grid item xs={12} sm={6} md={4} key={proyecto.id}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {proyecto.nombre}
                        </Typography>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          paragraph
                        >
                          {proyecto.descripcion}
                        </Typography>
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                          }}
                        >
                          <Chip
                            label={proyecto.estado}
                            color={
                              proyecto.estado === 'Activo'
                                ? 'success'
                                : 'default'
                            }
                          />
                          <Button
                            size="small"
                            onClick={() =>
                              navigate(`/dashboard/proyectos/${proyecto.id}`)
                            }
                          >
                            Ver Detalles
                          </Button>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home; 