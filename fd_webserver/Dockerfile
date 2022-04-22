FROM ros:melodic-ros-base

# HACK: http://stackoverflow.com/questions/25193161/chfn-pam-system-error-intermittently-in-docker-hub-builds
RUN ln -s -f /bin/true /usr/bin/chfn

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python-pip python build-essential curl gcc g++ make g++-multilib
#RUN curl -s http://lcas.lincoln.ac.uk/repos/public.key | apt-key add -
#RUN apt-key add /tmp/public.key
#RUN apt-add-repository http://lcas.lincoln.ac.uk/ubuntu/main
#repos/release

#RUN apt-get update && apt-get install -y ros-indigo-catkinized-downward python-pip python build-essential curl



RUN bash -c "source /opt/ros/melodic/setup.bash; rosdep update"
RUN curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -

RUN apt-get install -y nodejs 
RUN dpkg -L nodejs

RUN pip install Flask
RUN npm install -g webpack@3.11.0 yarn

RUN bash -c "source /opt/ros/melodic/setup.bash; mkdir -p /downward_planner/src; cd /downward_planner/src; catkin_init_workspace"
COPY ./catkinized_downward /downward_planner/src/catkinized_downward
RUN bash -c "source /opt/ros/melodic/setup.bash; cd /downward_planner; catkin_make install"



COPY ./fd_webserver /fastdownward
WORKDIR /fastdownward

# Install app requirements using pip
RUN yarn add node-sass
RUN yarn && yarn run production

CMD bash -c "source /opt/ros/indigo/setup.bash; python app.py"
