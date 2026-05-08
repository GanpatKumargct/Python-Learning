export const jobs = [
  {
    id: '1',
    title: 'Senior Frontend Engineer',
    description: 'We are looking for an experienced frontend engineer to lead our React architecture and build stunning UI/UX experiences.',
    location: 'Remote',
    openings_count: 2,
    is_active: true,
  },
  {
    id: '2',
    title: 'Backend Developer (Python)',
    description: 'Join our data platform team building scalable APIs in FastAPI and PostgreSQL.',
    location: 'New York, NY (Hybrid)',
    openings_count: 1,
    is_active: true,
  },
  {
    id: '3',
    title: 'Product Designer',
    description: 'Help shape the future of our ATS product through user research, wireframing, and high-fidelity prototyping.',
    location: 'Remote',
    openings_count: 1,
    is_active: false,
  }
];

export const applications = [
  {
    id: 'app-1',
    job_id: '1',
    full_name: 'Alice Johnson',
    email: 'alice@example.com',
    phone: '+1 (555) 123-4567',
    resume_link: 'https://drive.google.com/example/alice-resume',
    skills: ['React', 'TypeScript', 'Tailwind', 'Next.js'],
    education: 'B.S. Computer Science, Stanford',
    current_stage: 'HR Round',
    history: [
      { stage: 'Screening', date: '2023-10-01' },
      { stage: 'Technical Round', date: '2023-10-05' },
      { stage: 'HR Round', date: '2023-10-10' }
    ]
  },
  {
    id: 'app-2',
    job_id: '1',
    full_name: 'Bob Smith',
    email: 'bob@example.com',
    phone: '+1 (555) 987-6543',
    resume_link: 'https://drive.google.com/example/bob-resume',
    skills: ['Vue', 'JavaScript', 'CSS'],
    education: 'Self-taught',
    current_stage: 'Technical Round',
    history: [
      { stage: 'Screening', date: '2023-10-02' },
      { stage: 'Technical Round', date: '2023-10-07' }
    ]
  },
  {
    id: 'app-3',
    job_id: '2',
    full_name: 'Charlie Davis',
    email: 'charlie@example.com',
    phone: '+1 (555) 555-5555',
    resume_link: 'https://drive.google.com/example/charlie-resume',
    skills: ['Python', 'Django', 'FastAPI', 'PostgreSQL'],
    education: 'M.S. Data Science, MIT',
    current_stage: 'Screening',
    history: [
      { stage: 'Screening', date: '2023-10-12' }
    ]
  },
  {
    id: 'app-4',
    job_id: '1',
    full_name: 'Diana Prince',
    email: 'diana@example.com',
    phone: '+1 (555) 111-2222',
    resume_link: 'https://drive.google.com/example/diana-resume',
    skills: ['React', 'Node.js', 'AWS'],
    education: 'B.S. Software Engineering',
    current_stage: 'Founder Round',
    history: [
      { stage: 'Screening', date: '2023-09-20' },
      { stage: 'Technical Round', date: '2023-09-25' },
      { stage: 'HR Round', date: '2023-10-02' },
      { stage: 'Founder Round', date: '2023-10-08' }
    ]
  },
  {
    id: 'app-5',
    job_id: '2',
    full_name: 'Eve Carter',
    email: 'eve@example.com',
    phone: '+1 (555) 333-4444',
    resume_link: 'https://drive.google.com/example/eve-resume',
    skills: ['Python', 'FastAPI', 'Docker', 'Kubernetes'],
    education: 'B.S. Computer Engineering',
    current_stage: 'Technical Round',
    history: [
      { stage: 'Screening', date: '2023-10-15' },
      { stage: 'Technical Round', date: '2023-10-18' }
    ]
  },
  {
    id: 'app-6',
    job_id: '3',
    full_name: 'Frank Ocean',
    email: 'frank@example.com',
    phone: '+1 (555) 555-6666',
    resume_link: 'https://drive.google.com/example/frank-resume',
    skills: ['Figma', 'UI/UX', 'Adobe XD', 'Sketch'],
    education: 'B.A. Graphic Design',
    current_stage: 'Screening',
    history: [
      { stage: 'Screening', date: '2023-10-20' }
    ]
  },
  {
    id: 'app-7',
    job_id: '1',
    full_name: 'Grace Hopper',
    email: 'grace@example.com',
    phone: '+1 (555) 777-8888',
    resume_link: 'https://drive.google.com/example/grace-resume',
    skills: ['React', 'Redux', 'Jest', 'Webpack'],
    education: 'Ph.D. Computer Science',
    current_stage: 'Founder Round',
    history: [
      { stage: 'Screening', date: '2023-09-10' },
      { stage: 'Technical Round', date: '2023-09-15' },
      { stage: 'HR Round', date: '2023-09-22' },
      { stage: 'Founder Round', date: '2023-09-28' }
    ]
  },
  {
    id: 'app-8',
    job_id: '2',
    full_name: 'Henry Ford',
    email: 'henry@example.com',
    phone: '+1 (555) 999-0000',
    resume_link: 'https://drive.google.com/example/henry-resume',
    skills: ['Python', 'Django', 'Celery', 'Redis'],
    education: 'M.S. Software Engineering',
    current_stage: 'HR Round',
    history: [
      { stage: 'Screening', date: '2023-10-05' },
      { stage: 'Technical Round', date: '2023-10-12' },
      { stage: 'HR Round', date: '2023-10-19' }
    ]
  },
  {
    id: 'app-9',
    job_id: '3',
    full_name: 'Ivy Lee',
    email: 'ivy@example.com',
    phone: '+1 (555) 222-1111',
    resume_link: 'https://drive.google.com/example/ivy-resume',
    skills: ['Figma', 'Wireframing', 'Prototyping'],
    education: 'B.S. Interaction Design',
    current_stage: 'Technical Round',
    history: [
      { stage: 'Screening', date: '2023-10-10' },
      { stage: 'Technical Round', date: '2023-10-14' }
    ]
  },
  {
    id: 'app-10',
    job_id: '1',
    full_name: 'Jack Ryan',
    email: 'jack@example.com',
    phone: '+1 (555) 444-5555',
    resume_link: 'https://drive.google.com/example/jack-resume',
    skills: ['JavaScript', 'HTML', 'CSS', 'React'],
    education: 'Bootcamp Graduate',
    current_stage: 'Screening',
    history: [
      { stage: 'Screening', date: '2023-10-22' }
    ]
  }
];

export const STAGES = [
  'Screening',
  'Technical Round',
  'HR Round',
  'Founder Round'
];
