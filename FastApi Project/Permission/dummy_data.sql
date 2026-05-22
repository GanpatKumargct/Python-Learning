-- Dummy Data for RBAC Engine (Run this in pgAdmin Query Tool)

-- 1. Insert Role
-- We use a specific UUID so we can reference it in other tables
INSERT INTO roles (id, name, label, is_system, created_at)
VALUES ('11111111-1111-1111-1111-111111111111', 'hiring_manager', 'Hiring Manager', false, NOW());

-- 2. Insert Module Access
-- Grants the Hiring Manager access to the "ats" module
INSERT INTO module_access (id, role_id, module_name, can_access)
VALUES (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'ats', true);

-- 3. Insert Entity Permissions
-- Grants the Hiring Manager permission to list, view, create, edit, amend candidates
INSERT INTO entity_permissions (id, role_id, entity_name, can_list, can_view, can_create, can_edit, can_delete, can_amend, can_export)
VALUES (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'candidate', true, true, true, true, false, true, false);

-- 4. Insert Field Permissions
-- full_name: Read/Write
INSERT INTO field_permissions (id, role_id, entity_name, field_name, can_read, can_write, is_hidden)
VALUES (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'candidate', 'full_name', true, true, false);

-- salary: Read only
INSERT INTO field_permissions (id, role_id, entity_name, field_name, can_read, can_write, is_hidden)
VALUES (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'candidate', 'salary', true, false, false);

-- internal_notes: Hidden
INSERT INTO field_permissions (id, role_id, entity_name, field_name, can_read, can_write, is_hidden)
VALUES (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'candidate', 'internal_notes', false, false, true);

-- 5. Insert Record Assignment
-- Assigns a specific candidate record to a specific actor
-- Actor ID from our JSON example: 123e4567-e89b-12d3-a456-426614174000
-- Record ID from our JSON example: 987e6543-e21b-12d3-a456-426614174000
INSERT INTO record_assignments (id, entity_name, record_id, assigned_to, assigned_role, assigned_by, assigned_at, is_active)
VALUES (
    gen_random_uuid(), 
    'candidate', 
    '987e6543-e21b-12d3-a456-426614174000', 
    '123e4567-e89b-12d3-a456-426614174000', 
    'hiring_manager', 
    '123e4567-e89b-12d3-a456-426614174000', 
    NOW(), 
    true
);
