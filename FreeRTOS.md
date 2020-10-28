### FreeRTOS
- 需要一個 cpu timer irq, tick
- 有四種 heap 管理方式可以選
- vTaskStartScheduler會創一個優先權最低的 idle thread
- Scheduling, configUSE_PREEMPTION
    - preemptive
    - non-preemptive
- 需要較精確的應用時，vTaskDelayUntil會比vTaskDelay更準確
#### [Preemptive Scheduling](https://www.sciencedirect.com/topics/engineering/preemptive-scheduling)
- thread 中如果沒有 call taskDelay or taskDelayUntil, 在**non-preemptive**的情況下，就會固定在當下的thread中，不會切出去
- 在 preemptive scheduling 就算沒有主動讓出執行權(taskDelay)，一樣會切出去先執行更高優先權的thread
