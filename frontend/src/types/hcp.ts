export interface HCP {
  id: number;
  name: string;
  hospital: string | null;
  speciality: string | null;
  location: string | null;
  email: string | null;
  phone: string | null;
  notes: string | null;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface HCPCreate {
  name: string;
  hospital?: string;
  speciality?: string;
  location?: string;
  email?: string;
  phone?: string;
  notes?: string;
}
