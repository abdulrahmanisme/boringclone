import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = "https://vgxqynooaoexzdyhzjui.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneHF5bm9vYW9leHpkeWh6anVpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjE2NTA5OCwiZXhwIjoyMDU3NzQxMDk4fQ.biHoJ37KNWiAIQgkYdU_VGLRR1_JSH_AsqRzzqoQE6w";

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export default supabase; 