import React, { useEffect, useState } from 'react';
import { userService } from '../services/userService';
import { User } from '../types';

const Users: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    fetchUsers();
  }, [page, rowsPerPage]);

  const fetchUsers = async () => {
    try {
      const response = await userService.getUsers(page, rowsPerPage);
      setUsers(response.content);
      setTotal(response.totalElements);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  return (
    <div>
      {/* Render your users component code here */}
    </div>
  );
};

export default Users; 