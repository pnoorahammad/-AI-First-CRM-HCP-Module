export interface Interaction {
  id: number;
  user_id: number;
  hcp_id: number;
  date: string;
  time: string;
  visit_type: string;
  products_discussed: string[];
  samples_given: string[];
  feedback: string | null;
  notes: string | null;
  source: string;
  ai_summary: string | null;
  created_at: string;
  updated_at: string;
}

export interface InteractionCreate {
  hcp_id: number;
  date: string;
  time: string;
  visit_type: string;
  products_discussed?: string[];
  samples_given?: string[];
  feedback?: string;
  notes?: string;
  follow_up_date?: string;
  source?: string;
}
