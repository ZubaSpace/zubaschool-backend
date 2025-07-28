-- Public Schema: Subscription Plans
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

-- Enable RLS
ALTER TABLE public.subscription_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY sysadmin_access ON public.subscription_plans
    FOR ALL
    USING (auth.role() = 'sysadmin')
    WITH CHECK (auth.role() = 'sysadmin');

-- Public Schema: Tenants
CREATE TABLE public.tenants (
    tenant_id UUID PRIMARY KEY,
    school_name VARCHAR(255) NOT NULL,
    address TEXT,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    principal_name VARCHAR(100),
    subscription_plan_id UUID REFERENCES public.subscription_plans(plan_id),
    branding_config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Active'
);

-- Enable RLS
ALTER TABLE public.tenants ENABLE ROW LEVEL SECURITY;
CREATE POLICY sysadmin_access ON public.tenants
    FOR ALL
    USING (auth.role() = 'sysadmin')
    WITH CHECK (auth.role() = 'sysadmin');