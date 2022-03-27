import os
import pty
import signal
import tempfile

def start_context(context_name, context):
  if len(os.environ.get('SHCTX_NEXT_CONTEXT_FILE', '')) > 0:
    next_context_file = os.environ['SHCTX_NEXT_CONTEXT_FILE']
    with open(next_context_file, 'w') as file:
      file.write(context_name)
    os.kill(os.getppid(), signal.SIGKILL)
    return ''

  os.environ['SHCTX_ENTER'] = ''
  os.environ['SHCTX_EXIT'] = ''

  for parts in context:
    os.environ['SHCTX_ENTER'] += parts.get('enter', '') + '\n'
    os.environ['SHCTX_EXIT'] += parts.get('exit', '') + '\n'

  f = tempfile.NamedTemporaryFile()

  os.environ['SHCTX_CONTEXT'] = context_name
  os.environ['SHCTX_NEXT_CONTEXT_FILE'] = f.name

  pty.spawn(['./context.sh'])

  del os.environ['SHCTX_NEXT_CONTEXT_FILE']
  next_context = f.read().decode('utf-8').strip()
  f.close()

  return next_context

def get_context(context_name, config):
  context = config[context_name]
  used_contexts_names = context.get('use', [])
  selected_contexts = []

  for used_context_name in used_contexts_names:
    selected_contexts.append(config[used_context_name])

  context = config[context_name]
  selected_contexts.append(context)

  return selected_contexts
