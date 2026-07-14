export interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  due_date?: string;
  assignee_id?: number;
}

export interface User {
  id: number;
  username: string;
  full_name: string;
  role: string;
  is_active: boolean;
}
