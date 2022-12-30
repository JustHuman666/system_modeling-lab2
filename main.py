import pandas as pd

from process import Process
from create import Create
from model import Model

def imit_simple_model(create_delay: float, 
                      create_name: str,
                      process_delay: float,
                      process_name: str,
                      process_max_queue: int,
                      time: float,
                      distribution="exponential",
                      channels=1):
    create: Create = Create(create_delay)
    process: Process = Process(process_delay, channels)
    print(f"Id0: {create.id}, id1: {process.id}")
    create.next_element = process
    process.max_queue = process_max_queue
    create.name = create_name
    process.name = process_name
    create.distribution = distribution
    process.distribution = distribution
    elements_list = [create, process]
    model: Model = Model(elements_list)
    model.simulate(time)

def imit_table_model(max_queue_p1_list: list,
                     max_queue_p2_list: list,
                     max_queue_p3_list: list,
                     delay_create_list: list,
                     delay_p1_list: list,
                     delay_p2_list: list,
                     delay_p3_list: list,
                     time:float,
                     channels=1):
    dataframe_info = pd.DataFrame()
    records = []
    for index in range(len(max_queue_p1_list)):
        result, model_info = simulate_model(max_queue_p1_list[index],
                                            max_queue_p2_list[index],
                                            max_queue_p3_list[index],
                                            delay_create_list[index],
                                            delay_p1_list[index],
                                            delay_p2_list[index],
                                            delay_p3_list[index],
                                            time,
                                            channels=channels)
        records.append({**model_info, **result})
    dataframe_info = dataframe_info.append(records)
    dataframe_info.to_excel(f"results_{channels}_channels.xlsx")
    
def simulate_model(max_queue_p1: int,
                   max_queue_p2: int,
                   max_queue_p3: int,
                   delay_c: float,
                   delay_p1: float,
                   delay_p2: float,
                   delay_p3: float,
                   time: float,
                   channels=1) -> str:
    create = Create(delay_c)
    process_1 = Process(delay_p1, channels=channels)
    process_2 = Process(delay_p2, channels=channels)
    process_3 = Process(delay_p3, channels=channels)

    create.next_element = process_1
    process_1.next_element = [process_2]
    process_2.next_element = [process_3]

    print(f"Id0: {create.id}, id1: {process_1.id}, id2: {process_2.id}, id3: {process_3.id}")
    process_1.max_queue = max_queue_p1
    process_2.max_queue = max_queue_p2
    process_3.max_queue = max_queue_p3

    create.name = "Creator"
    process_1.name = "Processor1"
    process_2.name = "Processor2"
    process_3.name = "Processor3"

    elements_list = [create, process_1, process_2, process_3]
    for element in elements_list:
        element.distribution = "exponential"
    model = Model(elements_list)
    result = model.simulate(time)
    model_info = {
        'max_queue_process_1': max_queue_p1,
        'max_queue_process_2': max_queue_p2,
        'max_queue_process_3': max_queue_p3,
        'delay_create': delay_c,
        'delay_process_1': delay_p1,
        'delay_process_2': delay_p2,
        'delay_process_3': delay_p3,
        'processed_quantity_1': process_1.quantity,
        'processed_quantity_2': process_2.quantity,
        'processed_quantity_3': process_3.quantity,
        'processed_failed_1': process_1.failure,
        'processed_failed_2': process_2.failure,
        'processed_failed_3': process_3.failure
    }
    return result,  model_info

if __name__ == "__main__":
    # print(f"Imitation of simple model: \n")
    # imit_simple_model(2.0, "Creator", 1.0, "Processor", 5, 1000.0)

    max_queue_p1_list: list = [5, 4, 3, 2, 1, 2, 3, 4, 5, 6]
    max_queue_p2_list: list = [6, 5, 4, 3, 2, 1, 2, 3, 4, 5]
    max_queue_p3_list: list = [5, 5, 4, 4, 3, 3, 2, 2, 1, 1]
    delay_create_list: list = [2, 3, 4, 3, 5, 2, 6, 1, 7, 2]
    delay_p1_list: list = [3, 3, 4, 4, 5, 5, 6, 6, 1, 7]
    delay_p2_list: list = [2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    delay_p3_list: list = [1, 2, 3, 4, 5, 6, 6, 6, 7, 3]

    # print(f"Imitation of simple model with three processes: \n")
    # imit_table_model(max_queue_p1_list,
    #                  max_queue_p2_list,
    #                  max_queue_p3_list,
    #                  delay_create_list,
    #                  delay_p1_list,
    #                  delay_p2_list,
    #                  delay_p3_list,
    #                  1000.0)

    # print(f"Imitation of simple model with one process, but 2 channels: \n")
    # imit_simple_model(2.0, "Creator", 3.0, "Processor", 5, 1000.0, channels=4)

    print(f"Imitation of table model with three processes and few channels: \n")
    imit_table_model(max_queue_p1_list,
                     max_queue_p2_list,
                     max_queue_p3_list,
                     delay_create_list,
                     delay_p1_list,
                     delay_p2_list,
                     delay_p3_list,
                     1000.0,
                     channels=4)

