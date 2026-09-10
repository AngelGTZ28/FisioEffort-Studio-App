import { createClient} from '@supabase/supabase-js'

const supabaseUrl = 'https://wwanitmtxsnhcinpgyua.supabase.co'
const supabaseKey = 'sb_publishable_XlM1wRE87aY4ZdYV8rMGuQ_9Akr5pFM'

export const supabase = createClient(supabaseUrl, supabaseKey)