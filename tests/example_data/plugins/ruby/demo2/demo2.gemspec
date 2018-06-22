# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'demo2/version'

Gem::Specification.new do |spec|
  spec.name          = 'demo2'
  spec.version       = ''
  spec.authors       = ['']
  spec.email         = ['']

  spec.summary       = ''
  spec.description   = ''
  spec.homepage      = ""

  # Prevent pushing this gem to RubyGems.org. To allow pushes either set the 'allowed_push_host'
  # to allow pushing to a single host or delete this section to allow pushing to any host.
  if spec.respond_to?(:metadata)
    spec.metadata['allowed_push_host'] = "TODO: Set to 'http://mygemserver.com'"
  else
    raise "RubyGems 2.0 or newer is required to protect against public gem pushes."
  end

  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }

  spec.bindir = 'bin'
  spec.executables   = ''
  spec.require_paths = ['lib']

  spec.add_development_dependency 'bundler', '~> 1.12'
  spec.add_development_dependency 'rake', '~> 10.0'

  spec.add_runtime_dependency 'claide',                '>= 1.0.0', '< 2.0'
  spec.add_runtime_dependency 'xcodeproj',             '~> 1.5', '>= 1.5.0'
  spec.add_runtime_dependency 'gh_inspector',   '~> 1.0'
  spec.add_runtime_dependency 'colored',       '~> 1.2'
  spec.add_runtime_dependency 'rubyzip', '~> 1.2','>= 1.2.0'
  spec.add_runtime_dependency 'rest-client','~> 1.8','>= 1.8.0'
  spec.add_runtime_dependency 'mobile_provision','~> 1.1','>= 1.1.1'
  spec.add_runtime_dependency 'plist', '~> 3.2', '>= 3.2.0'
  spec.add_runtime_dependency 'xcpretty', '~> 0.2.8', '>= 0.2.8'

end
