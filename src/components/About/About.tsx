export function About() {
  return (
    <section id="about" className="section-container bg-gray-900/50">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-8 text-white">About Me</h2>
        <div className="grid md:grid-cols-2 gap-8 text-left">
          <div className="space-y-4">
            <p className="text-gray-300 leading-relaxed">
              Software engineer who found his calling in code after a year of med school.
              Started as a support agent at DoorLoop, earned a promotion to QA Engineer
              within a year, and now building software full-time while waiting on my
              next promotion to Software Engineer.
            </p>
            <p className="text-gray-300 leading-relaxed">
              Outside of work, I'm self-hosting side apps for my family, experimenting
              with AI models on a Linux server, and building small games in Godot.
              When I'm not at a keyboard, you'll find me rock climbing, hiking 20-mile
              trails, or gaming. I'm a firm believer in clever solutions over bought ones.
            </p>
          </div>
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white">Technologies</h3>
            <div className="flex flex-wrap gap-3">
              {[
                "React",
                "TypeScript",
                "React Native",
                "Expo",
                "Node.js",
                "MongoDB",
                "Godot",
                "Cloudflare",
                "Docker",
              ].map((tech) => (
                <span
                  key={tech}
                  className="px-5 py-2.5 bg-green-500/10 border border-green-500/30 rounded-full text-base text-green-400 font-medium"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
