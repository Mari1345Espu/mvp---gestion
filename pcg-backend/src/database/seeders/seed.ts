import { PrismaClient } from '@prisma/client';
import {
  roles,
  estados,
  getUsers,
  programas,
  proyectos,
  gruposInvestigacion,
  reportes,
} from './initialData';

const prisma = new PrismaClient();

async function main() {
  console.log('Iniciando el proceso de seed...');

  // Limpiar la base de datos
  console.log('Limpiando la base de datos...');
  await prisma.reporte.deleteMany();
  await prisma.proyecto.deleteMany();
  await prisma.programa.deleteMany();
  await prisma.grupoInvestigacion.deleteMany();
  await prisma.usuario.deleteMany();
  await prisma.estado.deleteMany();
  await prisma.rol.deleteMany();

  // Insertar roles
  console.log('Insertando roles...');
  for (const rol of roles) {
    await prisma.rol.create({
      data: rol,
    });
  }

  // Insertar estados
  console.log('Insertando estados...');
  for (const estado of estados) {
    await prisma.estado.create({
      data: estado,
    });
  }

  // Insertar usuarios
  console.log('Insertando usuarios...');
  const users = await getUsers();
  for (const user of users) {
    await prisma.usuario.create({
      data: user,
    });
  }

  // Insertar programas
  console.log('Insertando programas...');
  for (const programa of programas) {
    await prisma.programa.create({
      data: programa,
    });
  }

  // Insertar proyectos
  console.log('Insertando proyectos...');
  for (const proyecto of proyectos) {
    await prisma.proyecto.create({
      data: proyecto,
    });
  }

  // Insertar grupos de investigación
  console.log('Insertando grupos de investigación...');
  for (const grupo of gruposInvestigacion) {
    await prisma.grupoInvestigacion.create({
      data: grupo,
    });
  }

  // Insertar reportes
  console.log('Insertando reportes...');
  for (const reporte of reportes) {
    await prisma.reporte.create({
      data: reporte,
    });
  }

  console.log('¡Proceso de seed completado exitosamente!');
}

main()
  .catch((e) => {
    console.error('Error durante el proceso de seed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  }); 