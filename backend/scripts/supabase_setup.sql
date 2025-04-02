-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User_Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  full_name VARCHAR(255),
  phone_number VARCHAR(20),
  address TEXT,
  additional_info JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Pet_Types Table
CREATE TABLE IF NOT EXISTS pet_types (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(50) NOT NULL UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Breeds Table
CREATE TABLE IF NOT EXISTS breeds (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pet_type_id UUID NOT NULL REFERENCES pet_types(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(pet_type_id, name)
);

-- Pets Table
CREATE TABLE IF NOT EXISTS pets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  species VARCHAR(50) NOT NULL,
  breed VARCHAR(100),
  age INTEGER,
  gender VARCHAR(20),
  description TEXT,
  image_url TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'pending', 'adopted')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Adoption_Applications Table
CREATE TABLE IF NOT EXISTS adoption_applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
  adopter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  message TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'submitted' CHECK (status IN ('submitted', 'approved', 'rejected')),
  submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Visit_Schedules Table
CREATE TABLE IF NOT EXISTS visit_schedules (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
  adopter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
  message TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Success_Stories Table
CREATE TABLE IF NOT EXISTS success_stories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
  adopter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  image_url TEXT,
  published_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Resources Table
CREATE TABLE IF NOT EXISTS resources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  category VARCHAR(100) NOT NULL,
  author_id UUID REFERENCES users(id) ON DELETE SET NULL,
  published_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Set up Row-Level Security Policies for tables
-- Users RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY users_select_policy ON users FOR SELECT USING (true);
CREATE POLICY users_insert_policy ON users FOR INSERT WITH CHECK (auth.uid()::uuid = id);
CREATE POLICY users_update_policy ON users FOR UPDATE USING (auth.uid()::uuid = id);
CREATE POLICY users_delete_policy ON users FOR DELETE USING (auth.uid()::uuid = id);

-- Profiles RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY profiles_select_policy ON user_profiles FOR SELECT USING (true);
CREATE POLICY profiles_insert_policy ON user_profiles FOR INSERT WITH CHECK (auth.uid()::uuid = user_id);
CREATE POLICY profiles_update_policy ON user_profiles FOR UPDATE USING (auth.uid()::uuid = user_id);
CREATE POLICY profiles_delete_policy ON user_profiles FOR DELETE USING (auth.uid()::uuid = user_id);

-- Pets RLS
ALTER TABLE pets ENABLE ROW LEVEL SECURITY;
CREATE POLICY pets_select_policy ON pets FOR SELECT USING (true);
CREATE POLICY pets_insert_policy ON pets FOR INSERT WITH CHECK (auth.uid()::uuid = owner_id);
CREATE POLICY pets_update_policy ON pets FOR UPDATE USING (auth.uid()::uuid = owner_id);
CREATE POLICY pets_delete_policy ON pets FOR DELETE USING (auth.uid()::uuid = owner_id);

-- Adoption Applications RLS
ALTER TABLE adoption_applications ENABLE ROW LEVEL SECURITY;
CREATE POLICY applications_select_policy ON adoption_applications FOR SELECT USING (
  auth.uid()::uuid = adopter_id OR 
  auth.uid()::uuid IN (SELECT owner_id FROM pets WHERE id = pet_id)
);
CREATE POLICY applications_insert_policy ON adoption_applications FOR INSERT WITH CHECK (auth.uid()::uuid = adopter_id);
CREATE POLICY applications_update_policy ON adoption_applications FOR UPDATE USING (
  auth.uid()::uuid IN (SELECT owner_id FROM pets WHERE id = pet_id)
);
CREATE POLICY applications_delete_policy ON adoption_applications FOR DELETE USING (
  auth.uid()::uuid = adopter_id OR 
  auth.uid()::uuid IN (SELECT owner_id FROM pets WHERE id = pet_id)
);

-- Visit Schedules RLS
ALTER TABLE visit_schedules ENABLE ROW LEVEL SECURITY;
CREATE POLICY visits_select_policy ON visit_schedules FOR SELECT USING (
  auth.uid()::uuid = adopter_id OR 
  auth.uid()::uuid IN (SELECT owner_id FROM pets WHERE id = pet_id)
);
CREATE POLICY visits_insert_policy ON visit_schedules FOR INSERT WITH CHECK (auth.uid()::uuid = adopter_id);
CREATE POLICY visits_update_policy ON visit_schedules FOR UPDATE USING (
  auth.uid()::uuid = adopter_id OR 
  auth.uid()::uuid IN (SELECT owner_id FROM pets WHERE id = pet_id)
);
CREATE POLICY visits_delete_policy ON visit_schedules FOR DELETE USING (
  auth.uid()::uuid = adopter_id OR 
  auth.uid()::uuid IN (SELECT owner_id FROM pets WHERE id = pet_id)
);

-- Create indexes for performance
CREATE INDEX idx_pets_owner_id ON pets(owner_id);
CREATE INDEX idx_pets_status ON pets(status);
CREATE INDEX idx_adoption_applications_pet_id ON adoption_applications(pet_id);
CREATE INDEX idx_adoption_applications_adopter_id ON adoption_applications(adopter_id);
CREATE INDEX idx_adoption_applications_status ON adoption_applications(status);
CREATE INDEX idx_visit_schedules_pet_id ON visit_schedules(pet_id);
CREATE INDEX idx_visit_schedules_adopter_id ON visit_schedules(adopter_id);
CREATE INDEX idx_visit_schedules_status ON visit_schedules(status);

-- Seed data for pet types
INSERT INTO pet_types (name) VALUES
  ('Dog'),
  ('Cat'),
  ('Bird'),
  ('Small Animal'),
  ('Reptile'),
  ('Fish'),
  ('Horse')
ON CONFLICT (name) DO NOTHING;

-- Seed data for dog breeds
INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Labrador Retriever' FROM pet_types WHERE name = 'Dog'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'German Shepherd' FROM pet_types WHERE name = 'Dog'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Golden Retriever' FROM pet_types WHERE name = 'Dog'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'French Bulldog' FROM pet_types WHERE name = 'Dog'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Beagle' FROM pet_types WHERE name = 'Dog'
ON CONFLICT (pet_type_id, name) DO NOTHING;

-- Seed data for cat breeds
INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Siamese' FROM pet_types WHERE name = 'Cat'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Persian' FROM pet_types WHERE name = 'Cat'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Maine Coon' FROM pet_types WHERE name = 'Cat'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Bengal' FROM pet_types WHERE name = 'Cat'
ON CONFLICT (pet_type_id, name) DO NOTHING;

INSERT INTO breeds (pet_type_id, name)
SELECT id, 'Ragdoll' FROM pet_types WHERE name = 'Cat'
ON CONFLICT (pet_type_id, name) DO NOTHING;

-- Add triggers to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_modtime
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_user_profiles_modtime
BEFORE UPDATE ON user_profiles
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_pet_types_modtime
BEFORE UPDATE ON pet_types
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_breeds_modtime
BEFORE UPDATE ON breeds
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_pets_modtime
BEFORE UPDATE ON pets
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_adoption_applications_modtime
BEFORE UPDATE ON adoption_applications
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_visit_schedules_modtime
BEFORE UPDATE ON visit_schedules
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_success_stories_modtime
BEFORE UPDATE ON success_stories
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_resources_modtime
BEFORE UPDATE ON resources
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();