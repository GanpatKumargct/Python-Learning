-- 1. Create a Super Admin Role
INSERT INTO roles (id, name, label, created_by, created_at) 
VALUES ('22222222-2222-2222-2222-222222222223', 'super_admin', 'System Administrator', '11111111-1111-1111-1111-111111111111', NOW())
ON CONFLICT DO NOTHING;

-- 2. Assign the Super Admin Role to your default Admin User (Actor)
INSERT INTO actor_roles (id, actor_id, role_id, assigned_by, assigned_at) 
VALUES ('33333333-3333-3333-3333-333333333334', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222223', '11111111-1111-1111-1111-111111111111', NOW())
ON CONFLICT DO NOTHING;

-- 3. Grant Explicit ALL Permissions across Candidate and Job Requisition entities
INSERT INTO permissions (id, role_id, entity_name, action, scope, effect) VALUES
(gen_random_uuid()::varchar, '22222222-2222-2222-2222-222222222223', 'candidate', 'create', 'all', 'allow'),
(gen_random_uuid()::varchar, '22222222-2222-2222-2222-222222222223', 'candidate', 'read', 'all', 'allow'),
(gen_random_uuid()::varchar, '22222222-2222-2222-2222-222222222223', 'candidate', 'transition', 'all', 'allow'),
(gen_random_uuid()::varchar, '22222222-2222-2222-2222-222222222223', 'job_requisition', 'create', 'all', 'allow'),
(gen_random_uuid()::varchar, '22222222-2222-2222-2222-222222222223', 'job_requisition', 'read', 'all', 'allow'),
(gen_random_uuid()::varchar, '22222222-2222-2222-2222-222222222223', 'job_requisition', 'transition', 'all', 'allow')
ON CONFLICT DO NOTHING;
