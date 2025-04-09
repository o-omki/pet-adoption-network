-- SQL setup script for Supabase

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('adopter', 'individual', 'shelter', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT,
    additional_info JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Pet Types Table
CREATE TABLE IF NOT EXISTS pet_types (
    pet_type_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type_name VARCHAR(50) UNIQUE NOT NULL
);

-- Breeds Table
CREATE TABLE IF NOT EXISTS breeds (
    breed_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_type_id UUID REFERENCES pet_types(pet_type_id) ON DELETE CASCADE,
    breed_name VARCHAR(100) NOT NULL,
    UNIQUE(pet_type_id, breed_name)
);

-- Pets Table
CREATE TABLE IF NOT EXISTS pets (
    pet_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    owner_type VARCHAR(20) NOT NULL CHECK (owner_type IN ('shelter', 'individual')),
    name VARCHAR(100) NOT NULL,
    pet_type_id UUID REFERENCES pet_types(pet_type_id),
    breed_id UUID REFERENCES breeds(breed_id),
    age INTEGER,
    gender VARCHAR(10),
    description TEXT,
    image_url TEXT,
    status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available', 'pending', 'adopted')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Adoption Applications Table
CREATE TABLE IF NOT EXISTS adoption_applications (
    application_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES pets(pet_id) ON DELETE CASCADE,
    adopter_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    message TEXT,
    status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('submitted', 'approved', 'rejected')),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Success Stories Table
CREATE TABLE IF NOT EXISTS success_stories (
    story_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES pets(pet_id) ON DELETE CASCADE,
    adopter_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    story_title VARCHAR(255) NOT NULL,
    story_content TEXT NOT NULL,
    image_url TEXT,
    published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resources Table
CREATE TABLE IF NOT EXISTS resources (
    resource_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    author_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Visit Schedules Table
CREATE TABLE IF NOT EXISTS visit_schedules (
    visit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES pets(pet_id) ON DELETE CASCADE,
    adopter_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert some initial pet types
INSERT INTO pet_types (type_name) 
VALUES ('Dog'), ('Cat'), ('Bird'), ('Rabbit'), ('Hamster'), ('Guinea Pig'), ('Fish')
ON CONFLICT (type_name) DO NOTHING;

-- Create RLS policies for enhanced security
-- This should be adapted to match your actual security requirements
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY users_policy ON users FOR ALL USING (auth.uid() = user_id OR EXISTS (SELECT 1 FROM users WHERE user_id = auth.uid() AND role = 'admin'));

-- Add more RLS policies as needed for your application
