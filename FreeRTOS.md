### FreeRTOS
- 需要一個 cpu timer irq, tick
- 有四種 heap 管理方式可以選
- vTaskStartScheduler會創一個優先權最低的 idle thread, priority zero (tskIDLE_PRIORITY)
- Scheduling, configUSE_PREEMPTION
    - preemptive
    - non-preemptive
- 需要較精確的應用時，vTaskDelayUntil 會比 vTaskDelay 更準確
- Watchdog rest 要放在最高優先權的 thread，低優先權有可能永遠執行不到
- [Mutex 與 Semaphore 的差異](https://jasonblog.github.io/note/linux_system/mutex_yu_semaphore_zui_da_de_cha_yi_shi.html)
    - **Mutexes** and **Binary Semaphores** are very similar but have some subtle differences: Mutexes include a priority inheritance mechanism, binary semaphores do not. This makes **binary semaphores the better choice for implementing synchronisation (between tasks or between tasks and an interrupt)**, and mutexes the better choice for implementing simple mutual exclusion.
    - Binary semaphore
        - **xSemaphoreCreateBinary** 建立完，直接 take 是拿不到 key 的，但 Mutex 可以
        - 常用在不同 task 或中斷訊號的同步
    - Mutex
        - 只有拿到鎖(take) 的 task 才可以釋放鎖(give)
        - 在拿到鎖之後到釋放鎖之間，是可以被切走的，只是別的 task 拿不到 key
### [Deferred Interrupt Handling](https://www.freertos.org/deferred_interrupt_processing.html)
- 可以建立一個最高優先權的 thread 作 event handler，處理從中斷或是各地方來的 event

#### Real Time Scheduling
- Time Slicing Scheduling Policy: 
    - This is also known as a round-robin algorithm. In this algorithm, **all equal priority tasks get CPU in equal portions of CPU time**.
##### Non Preemptive Scheduling
- 如果沒有 call taskDelay or taskDelayUntil, 就會固定在當下的 task 中不會切出去

##### [Preemptive Scheduling](https://www.sciencedirect.com/topics/engineering/preemptive-scheduling)
- 在 preemptive scheduling 就算沒有主動讓出執行權 (taskDelay or taskDelayUntil)，一樣會切出去先執行 **大於等於自身優先權**的 task
    - 若有一個動作需要固定頻率精準的執行，就需要採用 preemptive + taskDelayUntil + 最高優先權
```c
/* A task being unblocked cannot cause an immediate
context switch if preemption is turned off. */
#if (  configUSE_PREEMPTION == 1 )
{
    /* Preemption is on, but a context switch should
    only be performed if the unblocked task has a
    priority that is equal to or higher than the
    currently executing task. */
    if( pxTCB->uxPriority >= pxCurrentTCB->uxPriority )
    {
        xSwitchRequired = pdTRUE;
    }
    ...
#endif /* configUSE_PREEMPTION */
```