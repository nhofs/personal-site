interface Project {
  title: string;
  description: string;
  technologies: string[];
  githubUrl: string;
  liveUrl?: string;
}

const projects: Project[] = [
  {
    title: "Family Hub",
    description:
      "A self-hosted family management app handling calendars, budgeting, task lists, secure vault storage, recipes, and contacts — all in one place.",
    technologies: ["React Native", "Expo", "MongoDB"],
    githubUrl: "https://github.com/nhofs",
  },
  {
    title: "Lingua",
    description:
      "Language learning tool that generates stories using a local AI model, with per-word translations, text-to-speech, typing practice, and phoneme-based speaking evaluation.",
    technologies: ["React Native", "Expo", "Python", "AI/ML"],
    githubUrl: "https://github.com/nhofs",
  },
  {
    title: "Turn-Based Combat",
    description:
      "A 2D turn-based game with animated attack sequences — characters walk up to targets, strike, and return to position. Built in Godot with procedural enemy spawning.",
    technologies: ["Godot", "GDScript"],
    githubUrl: "https://github.com/nhofs",
  },
];

function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="p-8 bg-gray-800/50 border border-gray-700 rounded-xl hover:border-green-500/50 transition-colors text-center">
      <h3 className="text-xl font-semibold text-white mb-3">{project.title}</h3>
      <p className="text-gray-400 mb-5">{project.description}</p>
      <div className="flex flex-wrap justify-center gap-2 mb-5">
        {project.technologies.map((tech) => (
          <span
            key={tech}
            className="px-3 py-1.5 text-sm bg-gray-700 rounded text-gray-300"
          >
            {tech}
          </span>
        ))}
      </div>
      <div className="flex justify-center gap-4">
        <a
          href={project.githubUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-gray-400 hover:text-white transition-colors"
        >
          GitHub →
        </a>
        {project.liveUrl && (
          <a
            href={project.liveUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-green-400 hover:text-green-300 transition-colors"
          >
            Live Demo →
          </a>
        )}
      </div>
    </div>
  );
}

export function Projects() {
  return (
    <section id="projects" className="section-container">
      <div className="max-w-6xl mx-auto w-full">
        <h2 className="text-3xl md:text-4xl font-bold mb-16 text-center text-white">
          Projects
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.title} project={project} />
          ))}
        </div>
      </div>
    </section>
  );
}
