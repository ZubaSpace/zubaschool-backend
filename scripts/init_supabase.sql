-- Public Schema: Tenants
CREATE TABLE public.tenants (
    tenant_id UUID PRIMARY KEY,
    school_name VARCHAR(255) NOT NULL,
    address TEXT,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    principal_name VARCHAR(100),
    subscription_plan_id UUID,
    branding_config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Active'
);

-- Enable RLS
ALTER TABLE public.tenants ENABLE ROW LEVEL SECURITY;
CREATE POLICY sysadmin_access ON public.tenants
    USING (auth.role() = 'sysadmin');

-- Sample subscription plan (for testing)
CREATE TABLE public.subscription_plans (
    plan_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    price_monthly DECIMAL(10,2) NOT NULL,
    price_yearly DECIMAL(10,2),
    features JSONB NOT NULL,
    max_users INTEGER NOT NULL,
    max_storage_mb INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO public.subscription_plans (plan_id, name, description, price_monthly, max_users, max_storage_mb, features)
VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    'Pro',
    'Advanced features for schools',
    99.99,
    500,
    1000,
    '[
        {"feature_id": "dashboard_access", "name": "Dashboard Access", "description": "View advanced dashboard", "enabled": true, "sidebar_item": true, "sidebar_icon": "fa-home", "sidebar_path": "/dashboard", "restricted_roles": []}
    ]'
);