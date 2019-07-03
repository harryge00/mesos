## Mesos-agent 执行容器命令

为了支持直接和 `mesos-agent` 交互，并执行 `exec/list/attach` 这些命令，在 `src/python/cli_new` 中添加了新的插件 `agent-container`。
目前支持的命令有：
```
# mesos agent-container list
```